#!/usr/bin/env python3
"""Apply quarantine_catalogue_overrides route_seed_nugget into osint_services.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OVERRIDES = REPO_ROOT / ".docs" / "analysis" / "quarantine_catalogue_overrides.json"
CATALOGUE = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    osint = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    by_id = {str(r["module_id"]): r for r in osint}
    patched: list[str] = []
    for mid, ov in overrides.items():
        route = ov.get("route_seed_nugget")
        if not route:
            continue
        row = by_id.get(mid)
        if not row:
            continue
        if row.get("route_seed_nugget") != route:
            row["route_seed_nugget"] = route
            patched.append(mid)

    print(f"patched={len(patched)}")
    for mid in sorted(patched):
        print(mid)

    if args.write:
        CATALOGUE.write_text(
            json.dumps(osint, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
