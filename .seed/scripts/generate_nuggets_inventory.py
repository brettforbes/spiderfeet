#!/usr/bin/env python3
"""Generate .seed/original_nuggets_table.md from nuggets.json + spiderfeet_map.tql."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SCAN_VARS = {
    "IP_ADDRESS": "ip",
    "IPV6_ADDRESS": "ipv6",
    "INTERNET_NAME": "hostname",
    "DOMAIN_NAME": "domain",
    "TCP_PORT_OPEN": "port",
    "UDP_PORT_OPEN": "udp_port",
    "EMAILADDR": "email",
    "OPERATING_SYSTEM": "os",
    "HTTP_CODE": "http_code",
    "ERROR_MESSAGE": "error",
    "WEBSERVER_TECHNOLOGY": "technology",
    "SOFTWARE_USED": "product",
}


def nugget_id_to_tql(nugget_id: str) -> str:
    return nugget_id.lower().replace("_", "-")


def row_md(tql: str, nugget_id: str, desc: str, scan: str) -> str:
    desc = desc.replace("|", "\\|")
    return f"| {tql} | {nugget_id} | {desc} | {scan} |"


def main() -> None:
    nuggets = json.loads((ROOT / ".docs/analysis/nuggets.json").read_text(encoding="utf-8"))
    tql_text = (ROOT / ".seed/spiderfeet_map.tql").read_text(encoding="utf-8")
    tql_entities = set(re.findall(r"entity ([a-z0-9-]+), sub nugget", tql_text))

    entities: list[tuple[str, str, str, str]] = []
    descriptors: list[tuple[str, str, str, str]] = []
    internal: list[tuple[str, str, str, str]] = []

    for n in sorted(nuggets, key=lambda x: x["nugget_id"]):
        nugget_id = n["nugget_id"]
        tql = nugget_id_to_tql(nugget_id)
        if tql not in tql_entities:
            # Still list; TypeQL may lag nuggets.json
            pass
        desc = n.get("nugget_description", "")
        ntype = n.get("nugget_type", "")
        scan = SCAN_VARS.get(nugget_id, "")
        row = (tql, nugget_id, desc, scan)
        if ntype in ("ENTITY", "SUBENTITY"):
            entities.append(row)
        elif ntype in ("DESCRIPTOR", "DATA"):
            descriptors.append(row)
        else:
            internal.append(row)

    lines = [
        "# Nugget Inventory",
        "",
        "Central inventory mapping TypeQL entity names to `nugget_id`, descriptions, and scan variable names.",
        "",
        "**Sources:** `.seed/spiderfeet_map.tql` · `.docs/analysis/nuggets.json`",
        "",
        "**Scan Variable Name** — field or path in CLI scan output when mapping to this nugget. "
        "Fill in incrementally; only obvious mappings are pre-filled.",
        "",
        "---",
        "",
        "## Current entities (`nugget_type`: ENTITY or SUBENTITY)",
        "",
        "| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |",
        "|--------------------|-----------|-------------------|-------------------|",
    ]
    lines.extend(row_md(*r) for r in entities)
    lines.extend(
        [
            "",
            "---",
            "",
            "## Current descriptors (`nugget_type`: DESCRIPTOR or DATA)",
            "",
            "| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |",
            "|--------------------|-----------|-------------------|-------------------|",
        ]
    )
    lines.extend(row_md(*r) for r in descriptors)

    if internal:
        lines.extend(
            [
                "",
                "---",
                "",
                "## Internal (excluded from entity/descriptor tables)",
                "",
                "| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |",
                "|--------------------|-----------|-------------------|-------------------|",
            ]
        )
        lines.extend(row_md(*r) for r in internal)

    lines.extend(
        [
            "",
            "---",
            "",
            "## Proposed new entities (to fill in)",
            "",
            "| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |",
            "|--------------------|-----------|-------------------|-------------------|",
            "| box | BOX | Box entity placeholder | |",
            "",
            "---",
            "",
            "## Proposed new descriptors (to fill in)",
            "",
            "| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |",
            "|--------------------|-----------|-------------------|-------------------|",
            "| tag | TAG | Tag descriptor placeholder | |",
            "",
        ]
    )

    out_path = ROOT / ".seed/original_nuggets_table.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} ({len(entities)} entities, {len(descriptors)} descriptors)")


if __name__ == "__main__":
    main()
