#!/usr/bin/env python3
"""Probe alternative seeds for modules that fail strict validation (Stage 4b).

Usage:
  poetry run python .seed/scripts/tune_test_seeds.py --tier none --write
  poetry run python .seed/scripts/tune_test_seeds.py --tier none --limit 20 --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.test_corpus import (  # noqa: E402
    merge_validation_results_into_registry,
    plan_validation_items,
    rows_from_seed_registry,
    summarize_registry_validation,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import load_module_test_seeds  # noqa: E402

DEFAULT_CANDIDATES: Dict[str, List[str]] = {
    "DOMAIN_NAME": ["bbc.co.uk", "google.com", "github.com", "microsoft.com", "example.com"],
    "INTERNET_NAME": ["bbc.co.uk", "google.com", "github.com", "zone-h.org"],
    "IP_ADDRESS": ["185.220.101.1", "8.8.8.8", "1.1.1.1", "91.198.174.192"],
    "EMAILADDR": ["admin@bbc.co.uk", "noreply@google.com", "test@gmail.com"],
    "COMPANY_NAME": ["Google LLC", "Microsoft Corporation", "British Broadcasting Corporation"],
    "USERNAME": ["google", "github", "spiderfoot"],
    "PHONE_NUMBER": ["+12125551234", "+442071838750", "+61412345678"],
}


def probe_module(
    api_base: str,
    *,
    module_id: str,
    consumed_nugget_id: str,
    candidates: List[str],
    timeout_seconds: int,
) -> Dict[str, Any] | None:
    url = f"{api_base.rstrip('/')}/scan_ui"
    for value in candidates:
        body = {
            "module_id": module_id,
            "consumed": {"nugget_id": consumed_nugget_id, "nugget_data": value},
            "wait": True,
            "timeout_seconds": timeout_seconds,
        }
        try:
            response = requests.post(url, json=body, timeout=timeout_seconds + 30)
        except requests.RequestException:
            continue
        if not response.ok:
            continue
        payload = response.json()
        produced = payload.get("produced") or []
        status = (payload.get("scan_record") or {}).get("status") or "UNKNOWN"
        if status == "FINISHED" and len(produced) > 0:
            return {
                "module_id": module_id,
                "consumed_nugget_id": consumed_nugget_id,
                "input_value": value,
                "produced_count": len(produced),
                "validated_produces": True,
                "status": status,
            }
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Tune module test seeds via scan_ui probes")
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--tier", default="none")
    parser.add_argument("--limit", type=int, default=0, help="Max failed modules to probe (0 = all)")
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--write", action="store_true", help="Merge wins into registry + CSV")
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
    failed = [
        item
        for item in items
        if not seeds.get(item["module_id"], {}).get(item["consumed_nugget_id"], {}).get(
            "validated_produces"
        )
    ]
    if args.limit:
        failed = failed[: args.limit]

    wins: List[Dict[str, Any]] = []
    for index, item in enumerate(failed, start=1):
        module_id = item["module_id"]
        consumed_id = item["consumed_nugget_id"]
        current = item["input_value"]
        candidates = DEFAULT_CANDIDATES.get(consumed_id, [current])
        ordered = [current] + [value for value in candidates if value != current]
        print(f"[{index}/{len(failed)}] {module_id} …", flush=True)
        result = probe_module(
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
                f"  WIN {consumed_id}={result['input_value']!r} produced={result['produced_count']}",
                flush=True,
            )
        else:
            print("  no win", flush=True)

    report_path = Path(args.report)
    report_path.write_text(json.dumps(wins, indent=2) + "\n", encoding="utf-8")
    cumulative = summarize_registry_validation(
        configured_modules=configured,
        subscription_tier=args.tier if args.tier != "all" else None,
    )
    print(json.dumps({"new_wins": len(wins), "cumulative": cumulative}, indent=2))
    print(f"Report: {report_path}")

    if args.write and wins:
        merge_validation_results_into_registry(wins)
        write_test_corpus_csv(rows_from_seed_registry())
        print("Updated module_test_seeds.json and test_nugget_data.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
