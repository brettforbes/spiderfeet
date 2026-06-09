#!/usr/bin/env python3
"""Probe alternative seeds for modules not yet smoke-validated (Stage 4b/4c).

Positive modules: find inputs that produce objects.
Negative modules: find clean inputs that yield clean_miss verdict.

Usage:
  poetry run python .seed/scripts/tune_test_seeds.py --tier none --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.fixture_categories import fixture_category_for_service  # noqa: E402
from spiderfeet.map.routes_catalog import service_by_module_id  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    CLEAN_INPUT_CANDIDATES,
    DIRTY_INPUT_CANDIDATES,
    fixture_kind_for_module,
    probe_negative_clean,
    probe_positive_candidates,
)
from spiderfeet.map.test_corpus import (  # noqa: E402
    merge_validation_results_into_registry,
    plan_validation_items,
    rows_from_seed_registry,
    summarize_registry_validation,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import (  # noqa: E402
    load_module_test_seeds,
    seed_coverage_complete,
    seed_entry,
)

DEFAULT_CANDIDATES: Dict[str, List[str]] = {
    "DOMAIN_NAME": ["bbc.co.uk", "google.com", "github.com", "microsoft.com", "example.com"],
    "INTERNET_NAME": ["bbc.co.uk", "google.com", "github.com", "zone-h.org"],
    "IP_ADDRESS": ["185.220.101.1", "8.8.8.8", "1.1.1.1", "91.198.174.192"],
    "EMAILADDR": ["admin@bbc.co.uk", "noreply@google.com", "test@gmail.com"],
    "COMPANY_NAME": ["Google LLC", "Microsoft Corporation", "British Broadcasting Corporation"],
    "USERNAME": ["google", "github", "spiderfoot"],
    "PHONE_NUMBER": ["+12125551234", "+442071838750", "+61412345678"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Tune module test seeds via scan_ui probes")
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--tier", default="none")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs" / "analysis" / "seed_tuning_probe_results.json"),
    )
    args = parser.parse_args()

    runtime = get_runtime()
    configured = runtime.config.get("__modules__", {})
    items = plan_validation_items(
        configured_modules=configured,
        subscription_tier=args.tier if args.tier != "all" else None,
    )
    seeds = load_module_test_seeds()
    pending = [
        item
        for item in items
        if not seed_coverage_complete(item["module_id"], item["consumed_nugget_id"])
    ]
    if args.limit:
        pending = pending[: args.limit]

    wins: List[Dict[str, Any]] = []
    hit_wins: List[Dict[str, Any]] = []

    for index, item in enumerate(pending, start=1):
        module_id = item["module_id"]
        consumed_id = item["consumed_nugget_id"]
        current = item["input_value"]
        svc = service_by_module_id(module_id) or {}
        kind = fixture_kind_for_module(module_id, consumed_id)
        if not seed_entry(module_id, consumed_id) and fixture_category_for_service(svc) == "negative":
            kind = "negative"

        print(f"[{index}/{len(pending)}] {module_id} ({kind}) …", flush=True)

        if kind == "negative":
            clean_pool = CLEAN_INPUT_CANDIDATES.get(consumed_id, [current])
            ordered = [current] + [v for v in clean_pool if v != current]
            result = probe_negative_clean(
                args.api_base,
                module_id=module_id,
                consumed_nugget_id=consumed_id,
                candidates=ordered,
                timeout_seconds=args.timeout,
            )
            if result:
                result["region"] = "US"
                result["notes"] = "Clean input not listed/blocked; negative-fixture"
                wins.append(result)
                print(
                    f"  NEG WIN {consumed_id}={result['input_value']!r} "
                    f"verdict={result.get('verdict')}",
                    flush=True,
                )
                dirty_pool = DIRTY_INPUT_CANDIDATES.get(consumed_id, [])
                if dirty_pool:
                    hit = probe_positive_candidates(
                        args.api_base,
                        module_id=module_id,
                        consumed_nugget_id=consumed_id,
                        candidates=dirty_pool,
                        timeout_seconds=args.timeout,
                    )
                    if hit:
                        hit["merge_target"] = "positive_hit"
                        hit["notes"] = "Dirty input confirms module can emit"
                        hit_wins.append(hit)
                        print(
                            f"  HIT WIN input={hit['input_value']!r} "
                            f"produced={hit['produced_count']}",
                            flush=True,
                        )
            else:
                print("  no negative win", flush=True)
            continue

        candidates = DEFAULT_CANDIDATES.get(consumed_id, [current])
        ordered = [current] + [value for value in candidates if value != current]
        result = probe_positive_candidates(
            args.api_base,
            module_id=module_id,
            consumed_nugget_id=consumed_id,
            candidates=ordered,
            timeout_seconds=args.timeout,
        )
        if result:
            if consumed_id == "IP_ADDRESS" and result["input_value"] == "185.220.101.1":
                result["region"] = "global"
                result["notes"] = "Tor exit node test IP; status=FINISHED"
            else:
                result["region"] = "US"
            wins.append(result)
            print(
                f"  WIN {consumed_id}={result['input_value']!r} "
                f"produced={result['produced_count']}",
                flush=True,
            )
        else:
            print("  no win", flush=True)

    report_path = Path(args.report)
    report_path.write_text(
        json.dumps({"wins": wins, "positive_hit_wins": hit_wins}, indent=2) + "\n",
        encoding="utf-8",
    )
    cumulative = summarize_registry_validation(
        configured_modules=configured,
        subscription_tier=args.tier if args.tier != "all" else None,
    )
    print(json.dumps({"new_wins": len(wins), "hit_wins": len(hit_wins), "cumulative": cumulative}, indent=2))
    print(f"Report: {report_path}")

    if args.write:
        if wins:
            merge_validation_results_into_registry(wins)
        if hit_wins:
            merge_validation_results_into_registry(hit_wins)
        if wins or hit_wins:
            write_test_corpus_csv(rows_from_seed_registry())
            print("Updated module_test_seeds.json and test_nugget_data.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
