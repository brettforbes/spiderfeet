#!/usr/bin/env python3
"""Promote quarantine modules whose route_seed_nugget is validated in module_test_seeds.json."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

QUARANTINE_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"
BATTERY_SCRIPT = REPO_ROOT / ".seed" / "scripts" / "run_quarantine_battery.py"


def _load_battery():
    spec = importlib.util.spec_from_file_location("run_quarantine_battery", BATTERY_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_promotion_results(*, include_negative: bool = True) -> list[dict]:
    quarantine = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    seeds = json.loads(SEEDS_JSON.read_text(encoding="utf-8")).get("seeds", {})
    results: list[dict] = []
    for svc in quarantine:
        mid = str(svc["module_id"])
        route = svc.get("route_seed_nugget")
        entry = seeds.get(mid, {}).get(route, {})
        if entry.get("validated_produces"):
            results.append({"module_id": mid, "classification": "validated_hit"})
        elif include_negative and entry.get("validated_negative"):
            results.append({"module_id": mid, "classification": "validated_negative"})
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print module ids that would be promoted without writing catalogues",
    )
    parser.add_argument(
        "--no-negative",
        action="store_true",
        help="Only promote validated_produces (skip validated_negative)",
    )
    args = parser.parse_args()

    results = build_promotion_results(include_negative=not args.no_negative)
    if args.dry_run:
        for row in results:
            print(row["module_id"])
        print(f"would promote {len(results)} modules", file=sys.stderr)
        return 0

    battery = _load_battery()
    promoted = battery.promote_validated_hits(results)
    remaining = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    print(f"promoted {len(promoted)} modules; quarantine remaining={len(remaining)}")
    for mid in promoted:
        print(mid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
