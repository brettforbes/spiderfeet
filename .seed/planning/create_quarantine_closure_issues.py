#!/usr/bin/env python3
"""Create GitHub issues for quarantine test closure batches (Stage 5)."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "quarantine_closure_manifest.json"
PLAN = ROOT / ".docs" / "analysis" / "quarantine_test_closure_plan.md"
REPO = "brettforbes/spiderFeet"
PARENT_EPIC = 722
DELAY_SEC = 2.5

BATCHES = {
    "SF-05-12": {
        "title": "Quarantine batch: route seed alignment (18 modules)",
        "labels": ["stage-5", "quarantine"],
        "modules": [
            "sfp_accounts",
            "sfp_countryname",
            "sfp_crossref",
            "sfp_dnsbrute",
            "sfp_dnscommonsrv",
            "sfp_dnsneighbor",
            "sfp_dnsraw",
            "sfp_dnszonexfer",
            "sfp_hosting",
            "sfp_junkfiles",
            "sfp_names",
            "sfp_phone",
            "sfp_pgp",
            "sfp_similar",
            "sfp_social",
            "sfp_subdomain_takeover",
            "sfp_tldsearch",
            "sfp_tool_retirejs",
        ],
        "body": """## Problem
18 quarantine modules have `module_test_seeds.json` entries on a different consumed nugget than catalogue `route_seed_nugget`, so route smoke tests skip validated seeds.

## Desired outcome
- `quarantine_catalogue_overrides.json` sets `route_seed_nugget` per module
- Misaligned seeds moved to the route nugget (see closure plan)
- `audit_quarantine_route_seeds.py` shows **6+ immediate passes** where seeds were already validated

## Tasks
1. Apply overrides in `quarantine_catalogue_overrides.json` (landed in closure PR)
2. Regenerate `quarantine_services.json` via `analyse_modules.py --quarantine-only --write-quarantine`
3. Run `run_quarantine_battery.py --only <batch>` and tune remaining `clean_miss` modules
4. Update closure plan issue table with evidence

## Spec
SPEC-003 R3-05-06, R3-05-07

## Parent
#{parent}

## Reference
`.docs/analysis/quarantine_test_closure_plan.md` § A + B
""",
    },
    "SF-05-13": {
        "title": "Quarantine batch: content extractor seed tuning (12 modules)",
        "labels": ["stage-5", "quarantine"],
        "modules": [
            "sfp_binstring",
            "sfp_cookie",
            "sfp_customfeed",
            "sfp_errors",
            "sfp_iban",
            "sfp_intfiles",
            "sfp_pageinfo",
            "sfp_sslcert",
            "sfp_strangeheaders",
            "sfp_webanalytics",
            "sfp_webframework",
            "sfp_webserver",
        ],
        "body": """## Problem
12 local content/header extractors return `clean_miss` on current route seeds — inputs lack markers the module regex/parser expects.

## Desired outcome
Each module has `validated_produces` or `validated_negative` on `route_seed_nugget`.

## Tasks
1. Inspect `handleEvent` / parsers in each `modules/sfp_*.py`
2. Craft `TARGET_WEB_CONTENT`, `WEBSERVER_HTTPHEADERS`, or upstream spider fixtures
3. Run `validate_test_seeds.py` / `run_quarantine_battery.py --write` per module
4. Document negative fixtures where production hit is inappropriate

## Spec
SPEC-003 R3-05-06

## Parent
#{parent}

## Reference
`.docs/analysis/quarantine_test_closure_plan.md` § C
""",
    },
    "SF-05-14": {
        "title": "Quarantine: WSL Ruby CLI install (cmseek, testssl.sh, whatweb)",
        "labels": ["stage-5", "quarantine"],
        "modules": [
            "sfp_tool_cmseek",
            "sfp_tool_testsslsh",
            "sfp_tool_whatweb",
        ],
        "body": """## Problem
Three CLI wrappers require Ruby/bash tooling that does not install reliably on Windows-native PATH.

## Desired outcome
- WSL2 Ubuntu install documented and probed
- Battery passes for all three modules from WSL or wrapper stubs
- Optional: extend `probe_cli_tools.py` for WSL detection

## Tasks
1. Follow `.docs/analysis/wsl_ruby_cli_runbook.md`
2. Run battery with `--timeout 300` per module
3. Promote on pass (`--promote`) or set `service_state: error` with evidence

## Spec
SPEC-003 R3-05-07; CLI epic #733

## Parent
#{parent}

## Reference
`.docs/analysis/wsl_ruby_cli_runbook.md`
""",
    },
    "SF-05-15": {
        "title": "Quarantine: blocked native CLI resolution (nbtscan, onesixtyone, wappalyzer)",
        "labels": ["stage-5", "quarantine"],
        "modules": [
            "sfp_tool_nbtscan",
            "sfp_tool_onesixtyone",
            "sfp_tool_wappalyzer",
        ],
        "body": """## Problem
Three CLI modules fail with `error_failed` — binaries unavailable or deprecated on Windows dev hosts.

## Options
| Module | Option A | Option B |
|--------|----------|----------|
| nbtscan | WSL `apt install nbtscan` | Document `service_state: error` |
| onesixtyone | WSL build from source | SNMP lab target + defer |
| wappalyzer | Retire module (npm CLI deprecated) | WSL + legacy fork |

## Desired outcome
Decision recorded; either battery pass via WSL or explicit retirement / error state in catalogue.

## Spec
SPEC-003 R3-05-07; CLI epic #733

## Parent
#{parent}

## Reference
`.docs/analysis/quarantine_test_closure_plan.md` § E
""",
    },
}


def gh_create(title: str, body: str, labels: list[str]) -> int:
    cmd = [
        "gh",
        "issue",
        "create",
        "--repo",
        REPO,
        "--title",
        title,
        "--body",
        body,
    ]
    for label in labels:
        cmd.extend(["--label", label])
    out = subprocess.check_output(cmd, text=True).strip()
    num = int(out.rsplit("/", 1)[-1])
    return num


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    manifest.setdefault("parent_epic", PARENT_EPIC)
    manifest.setdefault("plan", str(PLAN.relative_to(ROOT)))
    manifest.setdefault("issues", {})

    for key, spec in BATCHES.items():
        if key in manifest["issues"]:
            print(f"skip {key} -> #{manifest['issues'][key]}")
            continue
        body = spec["body"].format(parent=PARENT_EPIC)
        print(f"plan {key}: {spec['title']} ({len(spec['modules'])} modules)")
        if args.create:
            num = gh_create(spec["title"], body, spec["labels"])
            manifest["issues"][key] = num
            print(f"created #{num}")
            time.sleep(DELAY_SEC)

    manifest["batches"] = {
        k: {"modules": v["modules"], "title": v["title"]} for k, v in BATCHES.items()
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}")
    if not args.create:
        print("Dry run — pass --create to open GitHub issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
