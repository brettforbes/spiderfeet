#!/usr/bin/env python3
"""Create Stage 5 quarantine GitHub issues (idempotent via manifest)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "stage5_quarantine_manifest.json"
DELAY_SEC = 2.5

REPOS = {
    "spiderFeet": "brettforbes/spiderFeet",
    "spiderFeet-widget": "brettforbes/spiderFeet-widget",
}

CATEGORIES = {
    "SF-05-04": {
        "title": "Quarantine batch: DNS & Domain Intelligence (10 modules)",
        "modules": [
            "sfp_dnsbrute", "sfp_dnscommonsrv", "sfp_dnsneighbor", "sfp_dnsraw",
            "sfp_dnsresolve", "sfp_dnszonexfer", "sfp_similar", "sfp_subdomain_takeover",
            "sfp_tldsearch", "sfp_whois",
        ],
    },
    "SF-05-05": {
        "title": "Quarantine batch: Web Crawling & Scanning (6 modules)",
        "modules": [
            "sfp_crossref", "sfp_intfiles", "sfp_junkfiles", "sfp_portscan_tcp",
            "sfp_spider", "sfp_sslcert",
        ],
    },
    "SF-05-06": {
        "title": "Quarantine batch: Content Analysis & Extraction (21 modules)",
        "modules": [
            "sfp_base64", "sfp_binstring", "sfp_bitcoin", "sfp_company", "sfp_cookie",
            "sfp_countryname", "sfp_creditcard", "sfp_email", "sfp_errors", "sfp_ethereum",
            "sfp_filemeta", "sfp_hashes", "sfp_hosting", "sfp_iban", "sfp_names",
            "sfp_pageinfo", "sfp_phone", "sfp_strangeheaders", "sfp_webanalytics",
            "sfp_webframework", "sfp_webserver",
        ],
    },
    "SF-05-07": {
        "title": "Quarantine batch: Social & Identity (2 modules)",
        "modules": ["sfp_accounts", "sfp_social"],
    },
    "SF-05-08": {
        "title": "Quarantine batch: Reputation (1 module)",
        "modules": ["sfp_customfeed"],
    },
    "SF-05-09": {
        "title": "Quarantine batch: Public Registries (1 module)",
        "modules": ["sfp_pgp"],
    },
    "SF-05-10": {
        "title": "Quarantine batch: External Tool Wrappers (13 modules)",
        "modules": [
            "sfp_tool_cmseek", "sfp_tool_dnstwist", "sfp_tool_nbtscan", "sfp_tool_nmap",
            "sfp_tool_nuclei", "sfp_tool_onesixtyone", "sfp_tool_retirejs",
            "sfp_tool_snallygaster", "sfp_tool_testsslsh", "sfp_tool_trufflehog",
            "sfp_tool_wafw00f", "sfp_tool_wappalyzer", "sfp_tool_whatweb",
        ],
    },
}

MODULE_NAMES = {
    "sfp_dnsbrute": "DNS Brute-forcer",
    "sfp_dnscommonsrv": "DNS Common SRV",
    "sfp_dnsneighbor": "DNS Look-aside",
    "sfp_dnsraw": "DNS Raw Records",
    "sfp_dnsresolve": "DNS Resolver",
    "sfp_dnszonexfer": "DNS Zone Transfer",
    "sfp_similar": "Similar Domain Finder",
    "sfp_subdomain_takeover": "Subdomain Takeover Checker",
    "sfp_tldsearch": "TLD Searcher",
    "sfp_whois": "Whois",
    "sfp_crossref": "Cross-Referencer",
    "sfp_intfiles": "Interesting File Finder",
    "sfp_junkfiles": "Junk File Finder",
    "sfp_portscan_tcp": "Port Scanner - TCP",
    "sfp_spider": "Web Spider",
    "sfp_sslcert": "SSL Certificate Analyzer",
    "sfp_base64": "Base64 Decoder",
    "sfp_binstring": "Binary String Extractor",
    "sfp_bitcoin": "Bitcoin Finder",
    "sfp_company": "Company Name Extractor",
    "sfp_cookie": "Cookie Extractor",
    "sfp_countryname": "Country Name Extractor",
    "sfp_creditcard": "Credit Card Number Extractor",
    "sfp_email": "E-Mail Address Extractor",
    "sfp_errors": "Error String Extractor",
    "sfp_ethereum": "Ethereum Address Extractor",
    "sfp_filemeta": "File Metadata Extractor",
    "sfp_hashes": "Hash Extractor",
    "sfp_hosting": "Hosting Provider Identifier",
    "sfp_iban": "IBAN Number Extractor",
    "sfp_names": "Human Name Extractor",
    "sfp_pageinfo": "Page Information",
    "sfp_phone": "Phone Number Extractor",
    "sfp_strangeheaders": "Strange Header Identifier",
    "sfp_webanalytics": "Web Analytics Extractor",
    "sfp_webframework": "Web Framework Identifier",
    "sfp_webserver": "Web Server Identifier",
    "sfp_accounts": "Account Finder",
    "sfp_social": "Social Network Identifier",
    "sfp_customfeed": "Custom Threat Feed",
    "sfp_pgp": "PGP Key Servers",
    "sfp_tool_cmseek": "Tool - CMSeeK",
    "sfp_tool_dnstwist": "Tool - DNSTwist",
    "sfp_tool_nbtscan": "Tool - nbtscan",
    "sfp_tool_nmap": "Tool - Nmap",
    "sfp_tool_nuclei": "Tool - Nuclei",
    "sfp_tool_onesixtyone": "Tool - onesixtyone",
    "sfp_tool_retirejs": "Tool - Retire.js",
    "sfp_tool_snallygaster": "Tool - snallygaster",
    "sfp_tool_testsslsh": "Tool - testssl.sh",
    "sfp_tool_trufflehog": "Tool - TruffleHog",
    "sfp_tool_wafw00f": "Tool - WAFW00F",
    "sfp_tool_wappalyzer": "Tool - Wappalyzer",
    "sfp_tool_whatweb": "Tool - WhatWeb",
}


def gh_json(args: list[str], payload: dict | None = None) -> dict:
    cmd = ["gh", "api", *args]
    if payload is not None:
        cmd.extend(["--input", "-"])
        p = subprocess.run(cmd, input=json.dumps(payload).encode(), capture_output=True)
    else:
        p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode() or p.stdout.decode())
    return json.loads(p.stdout) if p.stdout.strip() else {}


def ensure_label(repo: str, name: str, color: str, desc: str) -> None:
    try:
        gh_json(["-X", "POST", f"repos/{repo}/labels", "-f", f"name={name}", "-f", f"color={color}", "-f", f"description={desc}"])
    except RuntimeError:
        pass


def create_issue(repo: str, title: str, body: str, labels: list[str]) -> int:
    data = gh_json(["-X", "POST", f"repos/{repo}/issues"], {"title": title, "body": body, "labels": labels})
    time.sleep(DELAY_SEC)
    return int(data["number"])


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"epics": {}, "framework": {}, "categories": {}, "modules": {}, "widget": {}, "cross_repo": {}}


def save_manifest(m: dict) -> None:
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")


def module_body(module_id: str, name: str, category_key: str, epic: int, batch: int) -> str:
    return f"""**Epic:** #{epic}
**Batch:** #{batch} (`{category_key}`)

## Problem statement

Quarantined module `{module_id}` (`{name}`) is not in `osint_services.json` / TypeDB map. It must become a full osint-service record and pass route testing before promotion.

## Scope

- [ ] Extract consumed/produced nuggets from `modules/{module_id}.py`
- [ ] Add catalogue row: `data_source`, `access_tier`, `module_opts`, `service_origin: quarantine`
- [ ] Icon: favicon URL or generated `icon_service_*.svg`
- [ ] Classify `fixture_category` (positive/negative) via smoke probe
- [ ] Add `module_test_seeds.json` + tune input until Tests pass
- [ ] Bootstrap TypeDB; set `service_state` (`in-test` or `error`)
- [ ] Outcome: **promoted** | **error** | **delete** (with rationale)

## Spec binding

- SPEC-003: R3-05-02, R3-05-03, R3-05-06, R3-05-07

## Reference

- `.docs/quarantine_modules.md` — `{module_id}`
- `.seed/planning/STAGE5_QUARANTINE_PROGRAM.md`
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    m = load_manifest()

    for repo in REPOS.values():
        for lab, color, desc in [
            ("stage-5", "6F42C1", "Stage 5 quarantine conversion"),
            ("quarantine", "E99695", "Quarantined module promotion"),
            ("cross-repo", "FEF2C0", "Cross-repo coordination"),
            ("spiderFeet-widget", "EDEDED", "Widget repo work"),
        ]:
            if not dry:
                ensure_label(repo, lab, color, desc)

    def epic(repo_key: str, key: str, title: str, body: str, labels: list[str]) -> int:
        if key in m["epics"]:
            return m["epics"][key]
        if dry:
            print(f"EPIC {key}: {title}")
            return 0
        num = create_issue(REPOS[repo_key], f"[Epic] {title}", body, ["epic"] + labels)
        m["epics"][key] = num
        save_manifest(m)
        return num

    def story(section: str, repo_key: str, key: str, title: str, body: str, labels: list[str], epic_num: int) -> int:
        store = m[section]
        if key in store:
            return store[key]
        full_body = f"**Epic:** #{epic_num}\n\n{body}" if epic_num else body
        if dry:
            print(f"  {key}: {title}")
            return 0
        num = create_issue(REPOS[repo_key], title, full_body, labels)
        store[key] = num
        save_manifest(m)
        return num

    sf_epic = epic(
        "spiderFeet", "EPIC-SF-05",
        "Stage 5 — Quarantine service conversion",
        """## Problem
54 quarantined modules lack osint-service catalogue records and map/test coverage.

## Outcome
Each module promoted, marked error, or removed with evidence. Full icons, data_source, seeds, route tests.

## Spec
`.governance/specs/SPEC-003-stage5-quarantine.md`

## Plan
`.seed/planning/STAGE5_QUARANTINE_PROGRAM.md`
""",
        ["stage-5"],
    )

    sfw_epic = epic(
        "spiderFeet-widget", "EPIC-SFW-05",
        "Stage 5 — Quarantine map & tests UI",
        """## Problem
Widget must display and test quarantine-origin services distinctly from Stage 4 external OSINT services.

## Outcome
Maps filter/styling; Tests plan includes quarantine modules; Subscriptions when keys required.

## Spec
SPEC-003 R3-05-05 (widget slice)
""",
        ["stage-5", "spiderFeet-widget"],
    )

    x_epic = epic(
        "spiderFeet", "EPIC-X-05",
        "Stage 5 — Custom OSINT service registration (spike)",
        """## Problem
Operators may want to register additional services (with or without API keys) beyond the built-in catalogue.

## Outcome
Architecture recommendation + spike; not necessarily full v1 implementation in Stage 5.

## Spec
SPEC-003 R3-05-08 (SPEC_GAP implementation path)
""",
        ["stage-5", "cross-repo"],
    )

    story("framework", "spiderFeet", "SF-05-01",
          "SPEC-003 + quarantine catalogue schema",
          """## Tasks
- [ ] Finalize SPEC-003 requirement IDs
- [ ] Define `service_origin`, `LOCAL_NOAUTH` model
- [ ] Document merge path into `osint_services.json`
- [ ] Update `analyse_modules.py` extraction rules

## Acceptance
Schema documented; team can add first quarantine row without ambiguity.
""",
          ["stage-5"], sf_epic)

    story("framework", "spiderFeet", "SF-05-02",
          "Infrastructure: catalogue merge + TypeDB bootstrap for quarantine",
          """## Tasks
- [ ] Staging or direct append to `osint_services.json`
- [ ] `bootstrap.py` / sync scripts handle `service_origin: quarantine`
- [ ] Maps graph includes quarantine services
- [ ] Tests API lists quarantine modules

## Depends on
#SF-05-01

## Acceptance
Empty shell record can be bootstrapped to TypeDB and appears on Maps.
""",
          ["stage-5"], sf_epic)

    story("framework", "spiderFeet", "SF-05-03",
          "Service icons for quarantine modules",
          """## Tasks
- [ ] Convention: `icon_service_{slug}.svg` in widget assets
- [ ] Source favicons for branded tools (nmap, nuclei, etc.)
- [ ] Generate SVG icons for local modules without brands
- [ ] Wire `data_source.fav_icon` / map node icon

## Acceptance
Every quarantine module has a visible icon on Maps.
""",
          ["stage-5"], sf_epic)

    for cat_key, cat in CATEGORIES.items():
        mod_lines = "\n".join(f"- [ ] `{mid}` — {MODULE_NAMES.get(mid, mid)}" for mid in cat["modules"])
        story("categories", "spiderFeet", cat_key, cat["title"],
              f"""## Modules ({len(cat['modules'])})

{mod_lines}

## Per-module work
See linked `[Quarantine]` issues. Each module: catalogue, icon, seeds, tests, promotion.

## Spec
R3-05-02, R3-05-06, R3-05-07
""",
              ["stage-5", "quarantine"], sf_epic)

    story("framework", "spiderFeet", "SF-05-11",
          "Custom OSINT service registration — backend spike",
          """## Tasks
- [ ] Options: TypeDB entity vs JSON catalogue extension vs plugin manifest
- [ ] Reuse Subscriptions secret opts for API keys
- [ ] Security boundary: no arbitrary user Python in v1
- [ ] Draft OpenAPI endpoints for CRUD custom services

## Epic
Cross-repo custom service program.

## Acceptance
Architecture doc + recommended v1 scope in issue comment.
""",
          ["stage-5", "cross-repo"], x_epic)

    story("widget", "spiderFeet-widget", "SFW-05-01",
          "Maps: quarantine service styling and filters",
          """## Tasks
- [ ] Visual distinction (colour/ring/badge) for `service_origin: quarantine`
- [ ] Filter bucket for quarantine vs external
- [ ] Legend update

## Depends on
Backend SF-05-02
""",
          ["stage-5", "spiderFeet-widget"], sfw_epic)

    story("widget", "spiderFeet-widget", "SFW-05-02",
          "Tests & Subscriptions: quarantine modules",
          """## Tasks
- [ ] Tests plan includes quarantine catalogue modules
- [ ] Subscriptions only when `access_tier` requires keys
- [ ] Signup metadata where external provider exists

## Depends on
Backend SF-05-02
""",
          ["stage-5", "spiderFeet-widget"], sfw_epic)

    story("widget", "spiderFeet-widget", "SFW-05-03",
          "Custom OSINT service registration — UI spike",
          """## Tasks
- [ ] UX flow: add service, credentials, consumed/produced nuggets
- [ ] Wire to backend spike (SF-05-11)
- [ ] Document out-of-scope for v1

## Acceptance
Mockup or stub page + issue comment with recommendation.
""",
          ["stage-5", "spiderFeet-widget", "cross-repo"], x_epic)

    # Per-module issues
    for cat_key, cat in CATEGORIES.items():
        batch_num = m["categories"].get(cat_key, 0)
        for mid in cat["modules"]:
            mod_key = f"Q-{mid}"
            if mod_key in m["modules"]:
                continue
            name = MODULE_NAMES.get(mid, mid)
            title = f"[Quarantine] {mid}: {name}"
            body = module_body(mid, name, cat_key, sf_epic, batch_num)
            if dry:
                print(f"    MOD {mod_key}")
                continue
            num = create_issue(REPOS["spiderFeet"], title, body, ["stage-5", "quarantine"])
            m["modules"][mod_key] = num
            save_manifest(m)

    save_manifest(m)
    print(f"Done. Epic SF={sf_epic}, SFW={sfw_epic}, X={x_epic}, modules={len(m['modules'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
