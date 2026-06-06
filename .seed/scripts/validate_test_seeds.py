#!/usr/bin/env python3
"""Validate module test seeds via live scan_ui (Stage 4b — SF-04B-06).

Usage:
  poetry run python .seed/scripts/validate_test_seeds.py --tier none --limit 40
  poetry run python .seed/scripts/validate_test_seeds.py --tier none --write
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
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


def run_scan_ui(
    api_base: str,
    *,
    module_id: str,
    consumed_nugget_id: str,
    input_value: str,
    timeout_seconds: int,
) -> Dict[str, Any]:
    url = f"{api_base.rstrip('/')}/scan_ui"
    body = {
        "module_id": module_id,
        "consumed": {"nugget_id": consumed_nugget_id, "nugget_data": input_value},
        "wait": True,
        "timeout_seconds": timeout_seconds,
    }
    try:
        response = requests.post(url, json=body, timeout=timeout_seconds + 30)
    except requests.RequestException as exc:
        return {
            "module_id": module_id,
            "consumed_nugget_id": consumed_nugget_id,
            "input_value": input_value,
            "status": "ERROR",
            "produced_count": 0,
            "validated_produces": False,
            "notes": str(exc),
        }
    if not response.ok:
        return {
            "module_id": module_id,
            "consumed_nugget_id": consumed_nugget_id,
            "input_value": input_value,
            "status": f"HTTP_{response.status_code}",
            "produced_count": 0,
            "validated_produces": False,
            "notes": response.text[:200],
        }
    payload = response.json()
    produced = payload.get("produced") or []
    status = (payload.get("scan_record") or {}).get("status") or "UNKNOWN"
    count = len(produced)
    return {
        "module_id": module_id,
        "consumed_nugget_id": consumed_nugget_id,
        "input_value": input_value,
        "status": status,
        "produced_count": count,
        "validated_produces": status == "FINISHED" and count > 0,
        "notes": "",
    }


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    tier_counts: Counter[str] = Counter()
    tier_pass: Counter[str] = Counter()
    for item, result in results:
        tier = item["subscription_tier"]
        tier_counts[tier] += 1
        if result.get("validated_produces"):
            tier_pass[tier] += 1
    by_tier = {
        tier: {
            "total": tier_counts[tier],
            "validated": tier_pass[tier],
            "rate_pct": round(100 * tier_pass[tier] / tier_counts[tier], 1)
            if tier_counts[tier]
            else 0.0,
        }
        for tier in sorted(tier_counts)
    }
    total = len(results)
    validated = sum(1 for _, r in results if r.get("validated_produces"))
    return {
        "total": total,
        "validated": validated,
        "rate_pct": round(100 * validated / total, 1) if total else 0.0,
        "by_tier": by_tier,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate module test seeds via scan_ui")
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--tier", default="none", help="Subscription tier filter (none, free_auth, paid_auth)")
    parser.add_argument("--limit", type=int, default=0, help="Max modules to validate (0 = all matching tier)")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N matching modules")
    parser.add_argument("--timeout", type=int, default=60, help="scan_ui timeout seconds per module")
    parser.add_argument("--write", action="store_true", help="Update registry JSON and test_nugget_data.csv")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs" / "analysis" / "test_seed_validation_report.json"),
        help="Write JSON summary report path",
    )
    args = parser.parse_args()

    runtime = get_runtime()
    items = plan_validation_items(
        configured_modules=runtime.config.get("__modules__", {}),
        subscription_tier=args.tier if args.tier != "all" else None,
        module_limit=args.limit or None,
        module_offset=args.offset,
    )
    if not items:
        print("No validation items for filter.", file=sys.stderr)
        return 1

    print(f"Validating {len(items)} modules (tier={args.tier})…")
    paired: List[tuple[Dict[str, Any], Dict[str, Any]]] = []
    for index, item in enumerate(items, start=1):
        print(f"[{index}/{len(items)}] {item['module_id']} …", flush=True)
        result = run_scan_ui(
            args.api_base,
            module_id=item["module_id"],
            consumed_nugget_id=item["consumed_nugget_id"],
            input_value=item["input_value"],
            timeout_seconds=args.timeout,
        )
        paired.append((item, result))
        mark = "PASS" if result.get("validated_produces") else "FAIL"
        print(
            f"  {mark} status={result.get('status')} produced={result.get('produced_count')}",
            flush=True,
        )

    summary = summarize(paired)
    cumulative = summarize_registry_validation(
        configured_modules=runtime.config.get("__modules__", {}),
        subscription_tier=args.tier if args.tier != "all" else None,
    )
    report = {
        "batch_summary": summary,
        "cumulative_registry": cumulative,
        "results": [
            {**item, **result}
            for item, result in paired
        ],
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"batch": summary, "cumulative": cumulative}, indent=2))
    print(f"Report: {report_path}")

    if args.write:
        merge_validation_results_into_registry(report["results"])
        write_test_corpus_csv(rows_from_seed_registry())
        print("Updated module_test_seeds.json and test_nugget_data.csv")

    target_rate = 60.0 if args.tier == "none" else 0.0
    if args.tier == "none" and cumulative["rate_pct"] < target_rate:
        print(
            f"Warning: none-tier cumulative pass rate {cumulative['rate_pct']}% below target {target_rate}%",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
