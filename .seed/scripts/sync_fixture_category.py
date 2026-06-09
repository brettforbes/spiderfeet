#!/usr/bin/env python3
"""Write fixture_category onto every row in osint_services.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.constants import OSINT_SERVICES_JSON  # noqa: E402
from spiderfeet.map.fixture_categories import fixture_category_for_service  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync fixture_category in osint_services.json")
    parser.add_argument("--write", action="store_true", help="Persist changes")
    args = parser.parse_args()

    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        rows = json.load(handle)

    positive = 0
    negative = 0
    for row in rows:
        category = fixture_category_for_service(row)
        row["fixture_category"] = category
        if category == "negative":
            negative += 1
        else:
            positive += 1

    print(f"modules={len(rows)} positive={positive} negative={negative}")
    if args.write:
        with OSINT_SERVICES_JSON.open("w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        print(f"wrote {OSINT_SERVICES_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
