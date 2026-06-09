#!/usr/bin/env python3
"""Set expected_absent_types on negative fixture registry entries from produced_nuggets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON, OSINT_SERVICES_JSON  # noqa: E402
from spiderfeet.map.test_targets import fixture_kind_for_entry, load_module_test_seeds  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        services = {row["module_id"]: row for row in json.load(handle)}

    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.get("seeds") or {}

    updated = 0
    for module_id, consumed_map in seeds.items():
        svc = services.get(module_id) or {}
        produced = [str(p) for p in (svc.get("produced_nuggets") or []) if p]
        if not produced:
            continue
        for consumed_id, entry in consumed_map.items():
            if not isinstance(entry, dict):
                continue
            if fixture_kind_for_entry(entry) != "negative":
                continue
            if entry.get("expected_absent_types"):
                continue
            entry["expected_absent_types"] = produced
            updated += 1
            print(f"set expected_absent_types {module_id} {consumed_id} ({len(produced)} types)")

    print(f"updated={updated}")
    if args.write and updated:
        with MODULE_TEST_SEEDS_JSON.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        load_module_test_seeds.cache_clear()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
