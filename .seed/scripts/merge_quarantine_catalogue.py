#!/usr/bin/env python3
"""Merge quarantine module records into osint_services.json (Stage 5 — R3-05-02)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".docs" / "analysis"))

from analyse_modules import analyse_quarantine_modules  # noqa: E402

CATALOGUE = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
STAGING = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"

# Refresh these fields from quarantine extract without demoting promoted modules.
_QUARANTINE_SYNC_KEYS = (
    "route_seed_nugget",
    "consumed_nuggets",
    "produced_nuggets",
    "consumption_group",
    "module_opts",
    "fixture_category",
    "service_origin",
)


def merge(*, write: bool, use_staging: bool) -> tuple[int, int, int]:
    if use_staging and STAGING.is_file():
        quarantine = json.loads(STAGING.read_text(encoding="utf-8"))
    else:
        quarantine = analyse_quarantine_modules()

    existing = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    by_id = {str(row["module_id"]): row for row in existing}
    added = 0
    updated = 0
    for svc in quarantine:
        mid = str(svc["module_id"])
        if mid in by_id:
            row = by_id[mid]
            origin = str(row.get("service_origin") or "")
            # Battery-promoted CLI tools: do not overwrite catalogue row.
            if row.get("service_state") == "in-test" and (
                origin in ("cli", "local")
                or (origin in ("external", "external-api") and mid.startswith("sfp_tool_"))
            ):
                continue
            for key in _QUARANTINE_SYNC_KEYS:
                if key in svc:
                    row[key] = svc[key]
            updated += 1
            continue
        by_id[mid] = svc
        added += 1

    for row in by_id.values():
        row.setdefault("service_origin", "external")

    merged = [by_id[k] for k in sorted(by_id)]
    print(f"catalogue total={len(merged)} added={added} origin_patched={updated} quarantine_extracted={len(quarantine)}")

    if write:
        CATALOGUE.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        STAGING.write_text(json.dumps(quarantine, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {CATALOGUE}")
        print(f"wrote {STAGING}")

    return len(merged), added, len(quarantine)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--staging-only", action="store_true", help="Read quarantine_services.json if present")
    args = parser.parse_args()
    merge(write=args.write, use_staging=args.staging_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
