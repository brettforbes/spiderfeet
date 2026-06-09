#!/usr/bin/env python3
"""Generate placeholder service icons for quarantine modules (SPEC-003 R3-05-04)."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QUARANTINE_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
WIDGET_ICONS = REPO_ROOT.parent / "spiderfeet-widget" / "src" / "assets" / "icons"
TEMPLATE = WIDGET_ICONS / "icon_software_used.svg"


def icon_filename(module_id: str) -> str:
    slug = module_id.replace("sfp_", "", 1) if module_id.startswith("sfp_") else module_id
    return f"icon_service_{slug}.svg"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Copy placeholder icons into widget assets")
    args = parser.parse_args()

    if not TEMPLATE.is_file():
        raise SystemExit(f"Template missing: {TEMPLATE}")
    if not QUARANTINE_JSON.is_file():
        raise SystemExit(f"Catalogue missing: {QUARANTINE_JSON}")

    rows = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    module_ids = [str(r["module_id"]) for r in rows if r.get("module_id")]
    created = 0
    skipped = 0

    for module_id in module_ids:
        dest = WIDGET_ICONS / icon_filename(module_id)
        if dest.is_file():
            skipped += 1
            continue
        if args.write:
            WIDGET_ICONS.mkdir(parents=True, exist_ok=True)
            shutil.copy2(TEMPLATE, dest)
        created += 1

    print(f"quarantine_modules={len(module_ids)} would_create={created} already_present={skipped}")
    if args.write and created:
        print(f"wrote {created} icons under {WIDGET_ICONS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
