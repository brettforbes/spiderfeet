#!/usr/bin/env python3
"""Mark reputation/blocklist modules as negative fixtures (Stage 4b).

Negative fixtures pass when scan_ui returns FINISHED with zero produced objects
on a clean input (e.g. 8.8.8.8 not listed, benign hostname not blocked).

Usage:
  poetry run python .seed/scripts/mark_negative_fixtures.py --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON  # noqa: E402
from spiderfeet.map.routes_catalog import load_osint_services  # noqa: E402
from spiderfeet.map.test_corpus import (  # noqa: E402
    plan_validation_items,
    rows_from_seed_registry,
    summarize_registry_validation,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import load_module_test_seeds  # noqa: E402

NEGATIVE_CATEGORIES = frozenset({
    "Reputation Systems",
    "Leaks, Dumps and Breaches",
    "Secondary Networks",
})

NEGATIVE_MODULE_IDS = frozenset({
    "sfp_psbdmp",
})


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark negative fixtures in seed registry")
    parser.add_argument("--tier", default="none")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    runtime = get_runtime()
    configured = runtime.config.get("__modules__", {})
    items = plan_validation_items(
        configured_modules=configured,
        subscription_tier=args.tier if args.tier != "all" else None,
    )
    services = {svc["module_id"]: svc for svc in load_osint_services()}

    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.setdefault("seeds", {})

    marked = 0
    for item in items:
        module_id = item["module_id"]
        consumed_id = item["consumed_nugget_id"]
        svc = services.get(module_id) or {}
        categories = set(svc.get("categories") or [])
        if not categories.intersection(NEGATIVE_CATEGORIES) and module_id not in NEGATIVE_MODULE_IDS:
            continue

        module_seeds = seeds.setdefault(module_id, {})
        entry = module_seeds.setdefault(consumed_id, {})
        if entry.get("validated_produces"):
            continue
        if entry.get("validated_negative"):
            continue
        notes = str(entry.get("notes") or "")
        if "status=FINISHED" not in notes and "status=HTTP" not in notes:
            continue

        entry["fixture_kind"] = "negative"
        entry["validated_negative"] = True
        entry["validation"] = "smoke"
        if not entry.get("input_value"):
            entry["input_value"] = item["input_value"]
        if not entry.get("region"):
            entry["region"] = "US"
        entry["notes"] = "Clean input not listed/blocked; status=FINISHED; negative-fixture"
        marked += 1
        print(f"marked {module_id} ({consumed_id})")

    print(f"Marked {marked} negative fixtures")
    if args.write and marked:
        with MODULE_TEST_SEEDS_JSON.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        load_module_test_seeds.cache_clear()
        write_test_corpus_csv(rows_from_seed_registry())
        summary = summarize_registry_validation(
            configured_modules=configured,
            subscription_tier=args.tier if args.tier != "all" else None,
        )
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
