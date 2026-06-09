#!/usr/bin/env python3
"""Pass 3: catalogue nugget probes + silent-search negative fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.routes_catalog import service_by_module_id  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    fetch_scan_log_summary,
    post_scan_ui,
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
from spiderfeet.map.test_targets import seed_coverage_complete  # noqa: E402

# Silent-search modules: benign input should yield clean_miss (negative fixture)
NEGATIVE_CLEAN: Dict[str, List[str]] = {
    "sfp_gravatar": ["noreply@example.com", "test@example.com"],
    "sfp_bgpview": ["8.8.8.8", "1.1.1.1"],
    "sfp_threatminer": ["8.8.8.8", "1.1.1.1"],
    "sfp_mnemonic": ["8.8.8.8", "1.1.1.1"],
    "sfp_digitaloceanspace": ["example.com", "sbs.com.au"],
    "sfp_google_tag_manager": ["example.com", "sbs.com.au"],
    "sfp_crxcavator": ["example.com", "sbs.com.au"],
    "sfp_s3bucket": ["example.com", "sbs.com.au"],
    "sfp_flickr": ["example.com", "sbs.com.au"],
}

# Catalogue nugget probes (pass 3 — after scan_ui target resolution fix)
POSITIVE_PROBE: Dict[str, List[str]] = {
    "sfp_gleif": ["Google LLC", "Microsoft Corporation", "Apple Inc."],
    "sfp_openstreetmap": [
        "1600 Amphitheatre Parkway, Mountain View, CA 94043",
        "10 Downing Street, London SW1A 2AA",
    ],
    "sfp_keybase": ["keybase", "github", "google"],
    "sfp_venmo": ["paypal", "venmo"],
    "sfp_google_tag_manager": ["GTM-WHNN", "GTM-5K8Q5L"],
    "sfp_crt": ["github.com", "stackoverflow.com"],
    "sfp_crobat_api": ["google.com", "microsoft.com"],
    "sfp_gravatar": ["admin@bbc.co.uk", "test@gmail.com"],
    "sfp_bgpview": ["91.198.174.192", "8.8.8.8"],
    "sfp_threatminer": ["8.8.8.8", "google.com"],
    "sfp_mnemonic": ["google.com", "github.com"],
    "sfp_digitaloceanspace": ["digitalocean.com"],
    "sfp_crxcavator": ["google.com", "github.com"],
    "sfp_s3bucket": ["github.com", "amazon.com"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs/analysis/pending_seed_research_pass3.json"),
    )
    args = parser.parse_args()

    items = plan_validation_items(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    pending = [
        i
        for i in items
        if not seed_coverage_complete(i["module_id"], i["consumed_nugget_id"])
    ]
    pending_ids = {i["module_id"] for i in pending}

    wins: List[Dict[str, Any]] = []
    negative_wins: List[Dict[str, Any]] = []
    findings: List[Dict[str, Any]] = []

    for mid, candidates in NEGATIVE_CLEAN.items():
        if mid not in pending_ids:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        print(f"[neg] {mid} …", flush=True)
        result = probe_negative_clean(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=args.timeout,
        )
        if result:
            svc = service_by_module_id(mid) or {}
            produced_types = list(svc.get("produced_nuggets") or [])
            result["fixture_kind"] = "negative"
            result["validated_negative"] = True
            result["region"] = "US"
            result["notes"] = "Pass 3 benign input; expect clean_miss (negative fixture)"
            if produced_types:
                result["expected_absent_types"] = produced_types
            negative_wins.append(result)
            print(f"  NEG OK {result['input_value']!r} verdict={result.get('verdict')}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=args.timeout,
                fixture_kind="negative",
            )
            findings.append({**item, **last, "phase": "negative", "outcome": "fail"})
            print(f"  NEG FAIL verdict={last.get('verdict')}", flush=True)

    for mid, candidates in POSITIVE_PROBE.items():
        if mid not in pending_ids:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        print(f"[pos] {mid} …", flush=True)
        result = probe_positive_candidates(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=args.timeout,
        )
        if result:
            result["region"] = "US"
            result["notes"] = "Pass 3 targeted probe; status=FINISHED"
            wins.append(result)
            print(f"  WIN {result['input_value']!r} produced={result['produced_count']}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=args.timeout,
                fixture_kind="positive",
            )
            logs = fetch_scan_log_summary(args.api_base, last.get("scan_id"), limit=12)
            findings.append({**item, **last, "phase": "positive", "log_snippet": logs})
            print(f"  miss verdict={last.get('verdict')} status={last.get('status')}", flush=True)

    report = {
        "positive_wins": wins,
        "negative_wins": negative_wins,
        "findings": findings,
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.write:
        if wins:
            merge_validation_results_into_registry(wins)
        if negative_wins:
            merge_validation_results_into_registry(negative_wins)
        if wins or negative_wins:
            write_test_corpus_csv(rows_from_seed_registry())
            print("Updated registry")

    cumulative = summarize_registry_validation(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    summary = {
        "positive_wins": len(wins),
        "negative_wins": len(negative_wins),
        "cumulative": cumulative,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
