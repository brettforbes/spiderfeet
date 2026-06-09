#!/usr/bin/env python3
"""Enrich quarantine module + osint_services records from battery results."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES = REPO_ROOT / "modules"
QUARANTINE_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
BATTERY_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_battery_results.json"
QUARANTINE_MD = REPO_ROOT / ".docs" / "quarantine_modules.md"

TOOL_INSTALL = {
    "sfp_tool_nmap": "Install Nmap and ensure `nmap` is on PATH.",
    "sfp_tool_nuclei": "Install ProjectDiscovery Nuclei; `nuclei` on PATH.",
    "sfp_tool_wappalyzer": "Install wappalyzer CLI or use the supported wrapper path.",
    "sfp_tool_whatweb": "Install WhatWeb (`whatweb` on PATH).",
    "sfp_tool_testsslsh": "Install testssl.sh and OpenSSL dependencies.",
    "sfp_tool_trufflehog": "Install TruffleHog v3+ (`trufflehog` on PATH).",
    "sfp_tool_wafw00f": "Install wafw00f (`wafw00f` on PATH).",
    "sfp_tool_retirejs": "Install retire.js CLI.",
    "sfp_tool_cmseek": "Install CMSeeK (`cmseek.py` or `cmsseek` on PATH).",
    "sfp_tool_dnstwist": "Install dnstwist (`dnstwist` on PATH).",
    "sfp_tool_nbtscan": "Install nbtscan.",
    "sfp_tool_onesixtyone": "Install onesixtyone SNMP scanner.",
    "sfp_tool_snallygaster": "Install snallygaster (`snallygaster` on PATH).",
}


def operation_summary(module_id: str, row: dict, battery: dict | None) -> str:
    summary = str(row.get("summary") or row.get("name") or module_id)
    consumed = row.get("consumed_nuggets") or []
    produced = row.get("produced_nuggets") or []
    parts = [
        summary.strip(),
        "",
        f"**Module ID:** `{module_id}`",
        f"**Origin:** quarantine (local SpiderFeet processing)",
        f"**Consumes:** {', '.join(consumed[:8])}{'…' if len(consumed) > 8 else ''}",
        f"**Produces:** {', '.join(produced[:8])}{'…' if len(produced) > 8 else ''}",
    ]
    flags = row.get("flags") or []
    if flags:
        parts.append(f"**Flags:** {', '.join(flags)}")
    if module_id in TOOL_INSTALL:
        parts.extend(["", "**Tool requirement:**", TOOL_INSTALL[module_id]])
    if battery:
        parts.extend(
            [
                "",
                "**Smoke battery:**",
                f"- Classification: `{battery.get('classification')}`",
                f"- Seed nugget: `{battery.get('consumed_nugget_id')}`",
                f"- Input: `{str(battery.get('input_value', ''))[:120]}`",
                f"- Produced count: {battery.get('produced_count', 0)}",
            ]
        )
        if battery.get("log_snippet"):
            parts.append(f"- Log: {battery['log_snippet'][:200]}")
    return "\n".join(parts)


def patch_module_docstring(module_path: Path, blurb: str) -> bool:
    text = module_path.read_text(encoding="utf-8")
    marker = "# Stage 5 operator documentation"
    block = (
        f"\n# {marker}\n"
        f"# {blurb.replace(chr(10), chr(10) + '# ')}\n"
    )
    if marker in text:
        return False
    # Insert after module header licence block
    match = re.search(r"(# -{10,}\n)\n", text)
    if not match:
        return False
    insert_at = match.end()
    new_text = text[:insert_at] + block + text[insert_at:]
    module_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    battery_rows = {}
    if BATTERY_JSON.is_file():
        payload = json.loads(BATTERY_JSON.read_text(encoding="utf-8"))
        for row in payload.get("results") or []:
            battery_rows[row["module_id"]] = row

    quarantine = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    osint = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    osint_by_id = {r["module_id"]: r for r in osint}

    patched_modules = 0
    for row in quarantine:
        mid = row["module_id"]
        battery = battery_rows.get(mid)
        desc = operation_summary(mid, row, battery)
        ds = row.setdefault("data_source", {})
        ds["description"] = desc
        ds.setdefault("website", f"spiderfeet://local/{mid}")
        ds.setdefault("model", "LOCAL_NOAUTH")
        if mid in TOOL_INSTALL:
            ds["api_key_instructions"] = [TOOL_INSTALL[mid]]
            ds["tool_requirement"] = TOOL_INSTALL[mid]

        if battery:
            cls = battery.get("classification")
            if cls == "validated_hit":
                row["service_state"] = "in-test"
            elif cls in ("tool_missing", "tool_missing_or_blocked"):
                row["service_state"] = "error"
            elif cls == "clean_miss":
                row["service_state"] = "in-test"
                row["fixture_category"] = row.get("fixture_category") or "negative"

        if mid in osint_by_id:
            osint_by_id[mid].update(row)
            osint_by_id[mid]["data_source"] = ds

        mod_path = MODULES / f"{mid}.py"
        if args.write and mod_path.is_file():
            short = (row.get("summary") or "")[:240]
            if patch_module_docstring(mod_path, short):
                patched_modules += 1

    if args.write:
        QUARANTINE_JSON.write_text(
            json.dumps(quarantine, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        OSINT_JSON.write_text(
            json.dumps(osint, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"updated catalogue; patched {patched_modules} module headers")
    else:
        print(f"dry-run: {len(quarantine)} services, battery={len(battery_rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
