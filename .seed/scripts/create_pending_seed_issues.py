#!/usr/bin/env python3
"""Create GitHub issues for pending none-tier seed research (Stage 4b)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.routes_catalog import service_by_module_id  # noqa: E402
from spiderfeet.map.test_corpus import plan_validation_items  # noqa: E402
from spiderfeet.map.test_targets import seed_coverage_complete  # noqa: E402

REPORT = REPO_ROOT / ".docs/analysis/test_seed_validation_report.json"
MANIFEST = REPO_ROOT / ".seed/planning/pending_seed_research_manifest.json"
EPIC_BODY = REPO_ROOT / ".seed/planning/issues/gh-SF-674-epic-body.md"


def pending_items() -> list[dict]:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    by_result = {x["module_id"]: x for x in report.get("results", [])}
    items = plan_validation_items(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    out = []
    for item in items:
        if seed_coverage_complete(item["module_id"], item["consumed_nugget_id"]):
            continue
        mid = item["module_id"]
        svc = service_by_module_id(mid) or {}
        res = by_result.get(mid, {})
        out.append(
            {
                **item,
                "name": svc.get("name") or mid,
                "summary": svc.get("summary") or "",
                "categories": svc.get("categories") or [],
                "produced_nuggets": svc.get("produced_nuggets") or [],
                "last_status": res.get("status"),
                "last_verdict": res.get("verdict"),
                "last_produced_count": res.get("produced_count"),
                "last_notes": res.get("notes", ""),
            }
        )
    return out


def issue_body(row: dict) -> str:
    cats = ", ".join(row.get("categories") or [])
    produced = ", ".join(row.get("produced_nuggets") or [])
    return f"""## Problem
Module `{row['module_id']}` has no smoke-validated entry in `module_test_seeds.json` (none-tier corpus gap).

## Last validation
| Field | Value |
|-------|-------|
| consumed | `{row['consumed_nugget_id']}` |
| input | `{row['input_value']}` |
| status | `{row.get('last_status')}` |
| verdict | `{row.get('last_verdict')}` |
| produced | `{row.get('last_produced_count')}` |

## Module
- **Name:** {row.get('name')}
- **Categories:** {cats}
- **Summary:** {row.get('summary')}
- **Produces:** {produced}

## Research tasks
1. Inspect `modules/{row['module_id']}.py` for required input shape and external API health.
2. Probe `POST /api/v1/scan_ui` with module-specific targets; use `GET /scans/{{id}}/logs` on failure.
3. Update `module_test_seeds.json` with validated input (or document `SPEC_GAP` / negative fixture if appropriate).
4. Run `poetry run python .seed/scripts/validate_test_seeds.py --tier none --write` for this module.

## Spec
R2-04-07 (module-validated test corpus)

## Parent epic
SF-674 — Pending none-tier seed research (32 modules)
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="Create issues via gh")
    parser.add_argument("--epic-only", action="store_true")
    args = parser.parse_args()

    rows = pending_items()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {MANIFEST}")

    if not args.create:
        print("Dry run — pass --create to open GitHub issues")
        return 0

    EPIC_BODY.parent.mkdir(parents=True, exist_ok=True)
    if not EPIC_BODY.is_file():
        EPIC_BODY.write_text(
            "## Problem\n"
            "32 none-tier OSINT modules lack smoke-validated seeds after automated tuning.\n\n"
            "## Outcome\n"
            "Per-module research issues (SF-675+) with validated `module_test_seeds.json` entries.\n\n"
            "## Spec\nR2-04-07\n",
            encoding="utf-8",
        )

    epic_url = subprocess.check_output(
        [
            "gh",
            "issue",
            "create",
            "--title",
            "SF-674: Epic — Pending none-tier seed research (32 modules)",
            "--label",
            "stage-4",
            "--body-file",
            str(EPIC_BODY),
        ],
        cwd=REPO_ROOT,
        text=True,
    ).strip()
    print(f"Epic: {epic_url}")
    epic_num = epic_url.rstrip("/").split("/")[-1]

    created = []
    start_num = 675
    for idx, row in enumerate(rows):
        num = start_num + idx
        slug = row["module_id"].replace("sfp_", "")
        body_path = REPO_ROOT / f".seed/planning/issues/gh-SF-{num}-body.md"
        body_path.write_text(issue_body(row), encoding="utf-8")
        url = subprocess.check_output(
            [
                "gh",
                "issue",
                "create",
                "--title",
                f"SF-{num}: Seed research — {row['module_id']}",
                "--label",
                "stage-4",
                "--body-file",
                str(body_path),
            ],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
        subprocess.run(
            ["gh", "issue", "comment", epic_num, "--body", f"Child: {url}"],
            cwd=REPO_ROOT,
            check=False,
        )
        created.append(url)
        print(url)

    print(f"Created {len(created)} issues under epic #{epic_num}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
