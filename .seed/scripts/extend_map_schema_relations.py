#!/usr/bin/env python3
"""Append missing osint-service relation subtypes + service_origin attribute to map schema."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA = REPO_ROOT / ".seed" / "spiderfeet_map.tql"
CATALOGUE = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"

RELATION_RE = re.compile(r"^\trelation (sfp-[a-z0-9-]+), sub osint-service;$")
ROUTE_SECTION = "\n\n\t#####################################\n\t# SpiderFeet Route Relation Definitions"


def kebab(module_id: str) -> str:
    return module_id.lower().replace("_", "-")


def load_existing_relations(text: str) -> set[str]:
    return {m.group(1) for line in text.splitlines() if (m := RELATION_RE.match(line))}


def ensure_service_origin(text: str) -> tuple[str, bool]:
    if "attribute service_origin" in text:
        return text, False
    if "owns service_state," in text and "owns service_origin," not in text:
        text = text.replace(
            "\t\towns service_state,",
            "\t\towns service_state,\n\t\towns service_origin,",
            1,
        )
    insert_attr = '\tattribute service_origin, value string @values("external", "quarantine", "custom");\n'
    marker = "\tattribute service_state, value string"
    if marker in text:
        text = text.replace(marker, insert_attr + marker, 1)
        return text, True
    return text, False


def append_relations(text: str, module_ids: list[str]) -> tuple[str, list[str]]:
    existing = load_existing_relations(text)
    missing = [mid for mid in module_ids if kebab(mid) not in existing]
    if not missing:
        return text, []

    block = "\n".join(f"\trelation {kebab(mid)}, sub osint-service;" for mid in missing)
    if ROUTE_SECTION not in text:
        raise RuntimeError("Route section marker not found in schema")
    text = text.replace(ROUTE_SECTION, f"\n{block}{ROUTE_SECTION}", 1)
    return text, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    rows = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    module_ids = [str(r["module_id"]) for r in rows if r.get("module_id")]
    text = SCHEMA.read_text(encoding="utf-8")
    text, origin_added = ensure_service_origin(text)
    text, added = append_relations(text, module_ids)
    print(f"service_origin_attr={'added' if origin_added else 'present'}")
    print(f"relation_subtypes_added={len(added)}")
    if added:
        print("  " + ", ".join(added[:8]) + ("..." if len(added) > 8 else ""))

    if args.write:
        SCHEMA.write_text(text, encoding="utf-8")
        print(f"wrote {SCHEMA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
