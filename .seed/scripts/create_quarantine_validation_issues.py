#!/usr/bin/env python3
"""Create validation epics and comment existing per-module issues with battery results."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = "brettforbes/spiderfeet"
REPO_WIDGET = "brettforbes/spiderfeet-widget"
ROOT = Path(__file__).resolve().parents[2]
BATTERY = ROOT / ".docs" / "analysis" / "quarantine_battery_results.json"
MANIFEST = ROOT / ".seed" / "planning" / "stage5_quarantine_manifest.json"
DELAY = 1.5


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    battery: dict[str, dict] = {}
    summary: dict[str, int] = {}
    if BATTERY.is_file():
        data = json.loads(BATTERY.read_text(encoding="utf-8"))
        summary = data.get("summary") or {}
        for row in data.get("results") or []:
            battery[row["module_id"]] = row

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    module_issues: dict[str, int] = {
        key.replace("Q-", ""): num
        for key, num in (manifest.get("modules") or {}).items()
    }

    epic_body = f"""## Problem

All 54 quarantine modules need external-service parity:
- smoke-validated `scan_ui` seeds
- rich `data_source.description` on OSINT service records
- module operator documentation
- distinct map icons

## Battery evidence (latest)

```json
{json.dumps(summary, indent=2)}
```

Artifacts:
- `.docs/analysis/quarantine_battery_results.json`
- `.docs/analysis/generic_icon_design_briefs.md` (70 icon briefs)
- `.seed/scripts/run_quarantine_battery.py`

**Spec:** SPEC-003 R3-05-06, R3-05-07  
**Parent:** #722
"""

    try:
        epic_url = gh(
            "issue", "create",
            "--repo", REPO,
            "--title", "Epic: Quarantine validation battery & documentation parity",
            "--body", epic_body,
        )
        print("epic:", epic_url)
        epic_num = epic_url.rstrip("/").split("/")[-1]
    except subprocess.CalledProcessError as exc:
        print(exc.stderr, file=sys.stderr)
        epic_num = "722"

    icon_body = """## Problem

70 map services still use the generic `icon_software_used.svg` placeholder.

## Deliverable

Single brief document: `.docs/analysis/generic_icon_design_briefs.md`

Each section is an agent-ready SVG spec (50×50, colours, metaphor, narrative).

## Acceptance

- [ ] Unique SVG per brief in `spiderfeet-widget/src/assets/icons/`
- [ ] Maps icon mode shows distinct glyphs

**Spec:** SPEC-003 R3-05-04  
**Parent:** #722
"""

    try:
        icon_url = gh(
            "issue", "create",
            "--repo", REPO_WIDGET,
            "--title", "Epic: Replace generic OSINT service map icons (70 briefs)",
            "--body", icon_body,
        )
        print("icon epic:", icon_url)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr, file=sys.stderr)

    for module_id, issue_num in sorted(module_issues.items()):
        row = battery.get(module_id, {})
        cls = row.get("classification", "pending")
        body = f"""## Validation battery update

**Classification:** `{cls}`  
**Consumed:** `{row.get('consumed_nugget_id', '?')}`  
**Input:** `{str(row.get('input_value', ''))[:200]}`  
**Produced:** {row.get('produced_count', '?')}  
**Verdict:** {row.get('verdict', '?')}

### Remaining work

- [ ] Tune seed until `validated_hit` or document `clean_miss` / `error`
- [ ] Enrich `data_source.description` + module header (Stage 5 docs block)
- [ ] Custom icon from `generic_icon_design_briefs.md`
- [ ] TypeDB `service_state` bootstrap after promotion

Evidence: `.docs/analysis/quarantine_battery_results.json`  
Program epic: #{epic_num}
"""
        try:
            gh(
                "issue", "comment", str(issue_num),
                "--repo", REPO,
                "--body", body,
            )
            print(f"commented #{issue_num} {module_id} ({cls})")
        except subprocess.CalledProcessError as exc:
            print(f"skip #{issue_num}: {exc.stderr}", file=sys.stderr)
        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
