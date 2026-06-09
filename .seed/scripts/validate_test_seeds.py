#!/usr/bin/env python3
"""Validate module test seeds via live scan_ui (Stage 4b/4c).

Positive fixtures: FINISHED + produced objects.
Negative fixtures: FINISHED + module_execution.verdict = clean_miss.

Usage:
  poetry run python .seed/scripts/validate_test_seeds.py --tier none --write
  poetry run python .seed/scripts/validate_test_seeds.py --tier none --offset 40 --limit 40 --write
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    fetch_scan_log_summary,
    fixture_kind_for_module,
    post_scan_ui,
    positive_hit_entry,
)
from spiderfeet.map.test_corpus import (  # noqa: E402
    merge_validation_results_into_registry,
    plan_validation_items,
    rows_from_seed_registry,
    summarize_registry_validation,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import seed_entry  # noqa: E402


def _passed(result: Dict[str, Any]) -> bool:
    return bool(result.get("validated_produces") or result.get("validated_negative"))


def summarize(paired: List[tuple[Dict[str, Any], Dict[str, Any]]]) -> Dict[str, Any]:
    tier_counts: Counter[str] = Counter()
    tier_pass: Counter[str] = Counter()
    for item, result in paired:
        tier = item["subscription_tier"]
        tier_counts[tier] += 1
        if _passed(result):
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
    total = len(paired)
    validated = sum(1 for _, r in paired if _passed(r))
    return {
        "total": total,
        "validated": validated,
        "rate_pct": round(100 * validated / total, 1) if total else 0.0,
        "by_tier": by_tier,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate module test seeds via scan_ui")
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--tier", default="none")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs" / "analysis" / "test_seed_validation_report.json"),
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
    hit_results: List[Dict[str, Any]] = []

    for index, item in enumerate(items, start=1):
        module_id = item["module_id"]
        consumed_id = item["consumed_nugget_id"]
        kind = fixture_kind_for_module(module_id, consumed_id)
        print(f"[{index}/{len(items)}] {module_id} ({kind}) …", flush=True)

        result = post_scan_ui(
            args.api_base,
            module_id=module_id,
            consumed_nugget_id=consumed_id,
            input_value=item["input_value"],
            timeout_seconds=args.timeout,
        )
        if not _passed(result):
            logs = fetch_scan_log_summary(args.api_base, result.get("scan_id"))
            if logs:
                result["notes"] = logs

        paired.append((item, result))
        mark = "PASS" if _passed(result) else "FAIL"
        print(
            f"  {mark} status={result.get('status')} "
            f"verdict={result.get('verdict')} produced={result.get('produced_count')}",
            flush=True,
        )

        entry = seed_entry(module_id, consumed_id)
        hit = positive_hit_entry(entry)
        hit_value = str(hit.get("input_value") or "").strip()
        if hit_value and kind == "negative":
            hit_result = post_scan_ui(
                args.api_base,
                module_id=module_id,
                consumed_nugget_id=consumed_id,
                input_value=hit_value,
                timeout_seconds=args.timeout,
                fixture_kind="positive",
            )
            hit_result["merge_target"] = "positive_hit"
            if hit_result.get("validated_produces"):
                hit_result["notes"] = "positive_hit smoke"
            hit_results.append(hit_result)
            print(
                f"  positive_hit {'PASS' if hit_result.get('validated_produces') else 'FAIL'} "
                f"input={hit_value!r} produced={hit_result.get('produced_count')}",
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
        "results": [{**item, **result} for item, result in paired],
        "positive_hit_results": hit_results,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"batch": summary, "cumulative": cumulative}, indent=2))
    print(f"Report: {report_path}")

    if args.write:
        merge_validation_results_into_registry(report["results"])
        if hit_results:
            merge_validation_results_into_registry(hit_results)
        write_test_corpus_csv(rows_from_seed_registry())
        print("Updated module_test_seeds.json and test_nugget_data.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
