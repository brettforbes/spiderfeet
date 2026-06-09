#!/usr/bin/env python3
"""Move dirty validated inputs on negative-category modules into positive_hit sub-seeds.

Primary seed becomes a clean input for clean_miss negative tests; dirty input is
retained under positive_hit for tuning (e.g. Tor exit IP on blocklists).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet import SpiderFeetHelpers  # noqa: E402
from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON, OSINT_SERVICES_JSON  # noqa: E402
from spiderfeet.map.fixture_categories import fixture_category_for_service  # noqa: E402
from spiderfeet.map.test_targets import load_module_test_seeds  # noqa: E402

_CLEAN_BY_NUGGET = {
    "IP_ADDRESS": "8.8.8.8",
    "IPV6_ADDRESS": "2001:4860:4860::8888",
    "INTERNET_NAME": "sbs.com.au",
    "DOMAIN_NAME": "sbs.com.au",
    "EMAILADDR": "noreply@spiderfoot.net",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        services = {row["module_id"]: row for row in json.load(handle)}

    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.get("seeds") or {}

    split = 0
    for module_id, consumed_map in seeds.items():
        svc = services.get(module_id) or {}
        if fixture_category_for_service(svc) != "negative":
            continue
        for consumed_id, entry in consumed_map.items():
            if not isinstance(entry, dict):
                continue
            if not entry.get("validated_produces"):
                continue
            if entry.get("positive_hit"):
                continue
            dirty = str(entry.get("input_value") or "").strip()
            clean = _CLEAN_BY_NUGGET.get(consumed_id)
            if not clean or dirty == clean:
                continue
            if SpiderFeetHelpers.targetTypeFromString(clean) is None:
                continue

            entry["positive_hit"] = {
                "input_value": dirty,
                "validated_produces": True,
                "notes": entry.get("notes") or "Dirty input confirms module can emit",
            }
            entry["input_value"] = clean
            entry["fixture_kind"] = "negative"
            entry["validated_negative"] = True
            entry.pop("validated_produces", None)
            entry["notes"] = "Clean input not listed/blocked; status=FINISHED; negative-fixture"
            split += 1
            print(f"split {module_id} {consumed_id}: clean={clean} hit={dirty}")

    print(f"split={split}")
    if args.write and split:
        with MODULE_TEST_SEEDS_JSON.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        load_module_test_seeds.cache_clear()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
