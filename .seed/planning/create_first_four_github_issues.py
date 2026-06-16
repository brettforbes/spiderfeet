#!/usr/bin/env python3
"""Create first-four-stage GitHub issues on spiderFeet + spiderFeet-widget. Idempotent via manifest."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ISSUE_URL_RE = re.compile(r"github\.com/[^/]+/[^/]+/issues/(\d+)")

ROOT = Path(__file__).resolve().parents[2]
OSINT_JSON = ROOT / ".docs/analysis/osint_services.json"
MANIFEST = Path(__file__).resolve().parent / "github_issues_manifest.json"
DELAY_SEC = 2.5  # avoid secondary rate limits on bulk issue create
RATE_LIMIT_SLEEP_SEC = 120

REPOS = {
    "spiderFeet": "brettforbes/spiderFeet",
    "spiderFeet-widget": "brettforbes/spiderFeet-widget",
}


def gh_json(args: list[str], input_json: dict | None = None) -> Any:
    cmd = ["gh", "api", *args]
    if input_json is not None:
        cmd.extend(["--input", "-"])
        p = subprocess.run(cmd, input=json.dumps(input_json).encode(), capture_output=True)
    else:
        p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode() or p.stdout.decode())
    if not p.stdout.strip():
        return {}
    return json.loads(p.stdout)


def _is_rate_limited(msg: str) -> bool:
    m = msg.lower()
    return "rate limit" in m or "secondary rate" in m or "temporarily blocked" in m


def gh_issue_create(repo: str, title: str, body: str, labels: list[str], retries: int = 12) -> int:
    """Create issue via REST API (reliable JSON) with label attachment."""
    owner, name = repo.split("/", 1)
    payload = {"title": title, "body": body, "labels": labels}
    last_err = ""
    for attempt in range(retries):
        try:
            data = gh_json(["-X", "POST", f"repos/{repo}/issues"], payload)
            return int(data["number"])
        except RuntimeError as err:
            last_err = str(err)
            if _is_rate_limited(last_err):
                time.sleep(RATE_LIMIT_SLEEP_SEC + attempt * 30)
                continue
            # Fallback: gh issue create (older gh without API convenience)
            cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
            for lab in labels:
                cmd.extend(["--label", lab])
            p = subprocess.run(cmd, capture_output=True, text=True)
            combined = f"{p.stdout}\n{p.stderr}"
            m = ISSUE_URL_RE.search(combined)
            if p.returncode == 0 and m:
                return int(m.group(1))
            last_err = p.stderr or p.stdout or last_err
            time.sleep(2)
    raise RuntimeError(f"issue create failed after {retries} tries: {last_err}")


def ensure_label(repo: str, name: str, color: str, description: str) -> None:
    try:
        gh_json(["-X", "POST", f"repos/{repo}/labels", "-f", f"name={name}", "-f", f"color={color}", "-f", f"description={description}"])
    except RuntimeError:
        pass  # already exists


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"created": {}, "epics": {}, "project": None}


def save_manifest(m: dict) -> None:
    MANIFEST.write_text(json.dumps(m, indent=2), encoding="utf-8")


def body_template(**sections: str) -> str:
    parts = []
    for k, v in sections.items():
        if v:
            parts.append(f"## {k}\n{v.strip()}\n")
    parts.append(
        "## Spec binding\n- SPEC-002 (first four stages) — requirement TBD at X-00-01\n\n"
        "## Board state\nBacklog — move to Ready when dependencies satisfied.\n"
    )
    return "\n".join(parts)


def create_epic(repo_key: str, key: str, title: str, body: str, labels: list[str], manifest: dict) -> int:
    ck = f"{repo_key}:{key}"
    if ck in manifest["epics"]:
        return manifest["epics"][ck]
    num = gh_issue_create(REPOS[repo_key], f"[Epic] {title}", body, ["epic"] + labels)
    manifest["epics"][ck] = num
    time.sleep(DELAY_SEC)
    return num


def create_story(repo_key: str, key: str, title: str, body: str, labels: list[str], epic_num: int | None, manifest: dict) -> int:
    if key in manifest["created"]:
        return manifest["created"][key]
    if epic_num:
        body = f"**Epic:** #{epic_num}\n\n{body}"
    num = gh_issue_create(REPOS[repo_key], title, body, labels)
    manifest["created"][key] = num
    time.sleep(DELAY_SEC)
    return num


def route_pairs() -> list[tuple[str, str, str, str]]:
    data = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    out = []
    for m in data:
        mid = m["module_id"]
        name = m.get("name", mid)
        for c in m.get("consumed_nuggets") or []:
            for p in m.get("produced_nuggets") or []:
                out.append((mid, name, c, p))
    return out


def main() -> int:
    manifest = load_manifest()
    only_routes = "--routes-only" in sys.argv
    skip_routes = "--skip-routes" in sys.argv

    for repo in REPOS.values():
        for lab, color, desc in [
            ("epic", "5319E7", "Epic / parent issue"),
            ("stage-0", "0E8A16", "Stage 0 governance"),
            ("stage-1", "1D76DB", "Stage 1 rebrand"),
            ("stage-2", "FBCA04", "Stage 2 FastAPI"),
            ("stage-3", "D93F0B", "Stage 3 TypeDB map"),
            ("stage-4", "B60205", "Stage 4 module testing"),
            ("route-test", "C5DEF5", "Per-route OSINT test"),
            ("cross-repo", "FEF2C0", "Cross-repo coordination"),
            ("spiderFeet-widget", "EDEDED", "Widget repo work"),
        ]:
            ensure_label(repo, lab, color, desc)

    if only_routes:
        skip_framework = True
    else:
        skip_framework = False

    if not skip_framework and not only_routes:
        # --- Stage 0 spiderFeet ---
        e = create_epic("spiderFeet", "EPIC-SF-00", "Stage 0 — Project governance (Python)",
                        body_template(**{"Problem": "Project-specific governance for Python backend.", "Outcome": "Rules in .governance/project and .cursor/rules."}),
                        ["stage-0"], manifest)
        for key, title, ac in [
            ("SF-00-01", "Audit generic vs project governance gap (spiderFeet)", "Matrix GOV vs project gaps documented."),
            ("SF-00-02", "Author Python-specific project rules", "Rules under .governance/project/rules/."),
            ("SF-00-03", "Mirror project rules to .cursor/rules/", "No drift from .governance/rules/."),
            ("SF-00-04", "Update PROJECT_INTENT for first-four program", "Links SPEC-002 and seed doc."),
            ("SF-00-05", "Extend BACKLOG.md with stage 0–4 traceability", "BL rows reference epics."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-0"], e, manifest)

        ew = create_epic("spiderFeet-widget", "EPIC-SFW-00", "Stage 0 — Project governance (Widget)",
                         body_template(**{"Problem": "Widget-specific governance.", "Outcome": "JS/iFrame rules mirrored."}),
                         ["stage-0", "spiderFeet-widget"], manifest)
        for key, title, ac in [
            ("SFW-00-01", "Audit governance gap (spiderFeet-widget)", "Matrix documented."),
            ("SFW-00-02", "Author JS/iFrame project rules", "Bootstrap, D3, API base URL conventions."),
            ("SFW-00-03", "Mirror widget rules to .cursor/rules/", "Parity with backend approach."),
            ("SFW-00-04", "Update widget PROJECT_INTENT.md", "Aligned with map UI program."),
            ("SFW-00-05", "Sync cursor-multi-repo skill in widget root", "Skill at .cursor/skills/cursor-multi-repo/."),
        ]:
            create_story("spiderFeet-widget", key, title, body_template(**{"Acceptance": ac}), ["stage-0", "spiderFeet-widget"], ew, manifest)

        ex = create_epic("spiderFeet", "EPIC-X-00", "Stage 0 — Program setup (cross-repo)",
                         body_template(**{"Problem": "Unified spec and workspace.", "Outcome": "SPEC-002 + multi-root workspace."}),
                         ["stage-0", "cross-repo"], manifest)
        for key, title, ac in [
            ("X-00-01", "Create SPEC-002-first-four-stages", "Requirement IDs for stages 0–4."),
            ("X-00-02", "Update multi-root workspace file", ".seed/spiderFeet_complete.code-workspace both roots."),
            ("X-00-03", "Link repos to GitHub Project (First Four)", "After gh project scope: add all issues to board."),
            ("X-00-04", "Import backlog items to project board", "BL + new issues on board."),
            ("X-00-05", "Operator sign-off: governance + SPEC-002", "Explicit approval before stage 1 execution."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-0", "cross-repo"], ex, manifest)

        # Stage 1
        e1 = create_epic("spiderFeet", "EPIC-SF-01", "Stage 1 — SpiderFeet rebrand (backend)",
                         body_template(**{"Outcome": "No SpiderFeet branding; Apache 2.0; 3 logos in README."}), ["stage-1"], manifest)
        for key, title, ac in [
            ("SF-01-01", "SpiderFeet reference inventory", "Report paths and counts."),
            ("SF-01-02", "Rename files and directories", "No spiderFeet path segments remain."),
            ("SF-01-03", "Update Python imports after rename", "Entry points run."),
            ("SF-01-04", "Replace strings and docs", "README and CLI say SpiderFeet."),
            ("SF-01-05", "Apache 2.0 license (Brett Forbes)", "MIT removed."),
            ("SF-01-06", "Three logo concepts in README", "Operator can choose."),
            ("SF-01-07", "Verify start.ps1 / dev entry", "Documented in README."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-1"], e1, manifest)

        e1w = create_epic("spiderFeet-widget", "EPIC-SFW-01", "Stage 1 — SpiderFeet rebrand (widget)",
                          body_template(**{"Outcome": "Widget branded; Apache 2.0."}), ["stage-1", "spiderFeet-widget"], manifest)
        for key, title, ac in [
            ("SFW-01-01", "Template → SpiderFeet naming pass", "package.json, README, UI strings."),
            ("SFW-01-02", "Apache 2.0 license (widget)", "LICENSE present."),
            ("SFW-01-03", "Three logo concepts in widget README", "Same concepts as backend."),
            ("SFW-01-04", "Confirm npm start / start.ps1", "Build and serve OK."),
            ("SFW-01-05", "Navbar placeholder branding", "Pending final logo."),
        ]:
            create_story("spiderFeet-widget", key, title, body_template(**{"Acceptance": ac}), ["stage-1", "spiderFeet-widget"], e1w, manifest)

        ex1 = create_epic("spiderFeet", "EPIC-X-01", "Stage 1 — Logo & rebrand sign-off",
                          body_template(**{"Outcome": "Final logo; grep sign-off."}), ["stage-1", "cross-repo"], manifest)
        for key, title, ac in [
            ("X-01-01", "Operator review: select final logo", "One logo chosen."),
            ("X-01-02", "Apply logo to widget navbar", "Visible in dist build."),
            ("X-01-03", "Repo-wide spiderFeet grep sign-off", "Allowlist file for exceptions."),
            ("X-01-04", "Close stage 1 epics", "Operator approval."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-1", "cross-repo"], ex1, manifest)

        # Stage 2
        e2 = create_epic("spiderFeet", "EPIC-SF-02", "Stage 2 — FastAPI over CLI",
                         body_template(**{"Outcome": "Swagger + Requestly proof."}), ["stage-2"], manifest)
        for key, title, ac in [
            ("SF-02-01", "CLI capability matrix", "sf.py flags → REST map."),
            ("SF-02-02", "FastAPI application skeleton", "Health, CORS, config."),
            ("SF-02-03", "start.ps1 for API server", "Documented host/port."),
            ("SF-02-04", "Scan-start API (-s parity)", "Returns scan id."),
            ("SF-02-05", "Module list API (-M parity)", "Matches CLI."),
            ("SF-02-06", "Event types API (-T parity)", "Matches CLI."),
            ("SF-02-07", "Scan status / results APIs", "Read progress and results."),
            ("SF-02-08", "OpenAPI + Swagger UI", "/docs accurate."),
            ("SF-02-09", "API reference documentation", ".docs/ updated."),
            ("SF-02-10", "Pytest suite in .tests/", "pytest passes."),
            ("SF-02-11", "Requestly collection & test plan", "Every endpoint documented."),
            ("SF-02-12", "Operator pairing: Requestly setup", "Collection imported."),
            ("SF-02-13", "Operator review: Requestly API sign-off", "Closes EPIC-SF-02."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-2"], e2, manifest)

        # Stage 3 backend
        e3a = create_epic("spiderFeet", "EPIC-SF-03A", "Stage 3a — TypeDB map ORM & seed",
                          body_template(**{"Outcome": "spiderFeet-map DB with schema + seed data."}), ["stage-3"], manifest)
        for key, title, ac in [
            ("SF-03A-01", "Externalise TypeDB connection JSON", "Injectable config."),
            ("SF-03A-02", "Type-bridge classes for spiderFeet_map.tql", "Core types covered."),
            ("SF-03A-03", "Type-bridge unit tests", "pytest insert/read."),
            ("SF-03A-04", "Idempotent DB bootstrap spiderFeet-map", "Safe re-run."),
            ("SF-03A-05", "Load archetype nuggets from nuggets.json", "Kebab-case entities."),
            ("SF-03A-06", "Load OSINT services from osint_services.json", "service-state=in-test."),
            ("SF-03A-07", "CLI/script entry for bootstrap", "No UI required."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-3"], e3a, manifest)

        e3b = create_epic("spiderFeet", "EPIC-SF-03B", "Stage 3b — FastAPI map CRUD & graph export",
                          body_template(**{"Outcome": "CRUD + nodes/edges API."}), ["stage-3"], manifest)
        for key, title, ac in [
            ("SF-03B-01", "Connection management API", "List/save/test connections."),
            ("SF-03B-02", "Trigger map DB init via API", "Calls bootstrap."),
            ("SF-03B-03", "CRUD APIs for nuggets", "Map model editable."),
            ("SF-03B-04", "CRUD APIs for osint-services", "Linkage updates."),
            ("SF-03B-05", "Force-graph export API", "nodes[] edges[] for D3."),
            ("SF-03B-06", "OpenAPI + pytest for map APIs", "Tests in .tests/."),
            ("SF-03B-07", "Extend start.ps1 for map APIs", "Single dev entry."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-3"], e3b, manifest)

        e3w = create_epic("spiderFeet-widget", "EPIC-SFW-03", "Stage 3c — Maps page & force graph UI",
                          body_template(**{"Outcome": "Maps tab functional; stub tabs empty."}), ["stage-3", "spiderFeet-widget"], manifest)
        stories_3w = [
            ("SFW-03-01", "Copy nugget icons to src/assets/icons/", "Icons from spiderFeet analysis."),
            ("SFW-03-02", "App shell: navbar, theme, five tabs", "Enrichments/Composer/Maps/Logs/Tests; non-Maps empty pages."),
            ("SFW-03-03", "Connection setup widget + gating", "Grey out until TypeDB connected."),
            ("SFW-03-04", "Maps page layout (Bootstrap 5)", "Full viewport graph."),
            ("SFW-03-05", "D3 force graph core render", "Colour scheme applied."),
            ("SFW-03-06", "OSINT service nodes 2× nugget", "Rounded square; state colours."),
            ("SFW-03-07", "fav_icon vs logo toggle", "Bootstrap switch."),
            ("SFW-03-08", "Edge styling and labels", "Min length 3× icon width."),
            ("SFW-03-09", "Legend bottom-right", "Node/edge types."),
            ("SFW-03-10", "Layout button panel", "Including grouped horizontal layout."),
            ("SFW-03-11", "Shadow nodes/edges toggle", "Predictable shadow IDs."),
            ("SFW-03-12", "Tooltips pretty-print JSON", "Hover nodes/edges."),
            ("SFW-03-13", "Zoom and pan", "Standard D3."),
            ("SFW-03-14", "Drag-fix and double-click reset", "Per spec."),
            ("SFW-03-15", "Filters: grouping + search", "grouping_of_osint_services.md dimensions."),
            ("SFW-03-16", "RMB context menu expand neighbours", "Progressive reveal."),
            ("SFW-03-17", "Light/dark mode", "force_graph_colour_scheme.md."),
            ("SFW-03-18", "Exploratory review: Maps page", "GOV-08 matrix complete."),
        ]
        for key, title, ac in stories_3w:
            create_story("spiderFeet-widget", key, title, body_template(**{"Acceptance": ac}), ["stage-3", "spiderFeet-widget"], e3w, manifest)

        # Stage 4 framework spiderFeet
        e4a = create_epic("spiderFeet", "EPIC-SF-04A", "Stage 4a — scan-record schema",
                          body_template(**{"Outcome": "scan-record in TypeDB."}), ["stage-4"], manifest)
        for key, title, ac in [
            ("SF-04A-01", "Extend spiderFeet_map.tql with scan-record", "Per §2.4.1."),
            ("SF-04A-02", "Type-bridge for scan-record and route", "CRUD helpers."),
            ("SF-04A-03", "Migrate bootstrap pipeline", "Safe re-init."),
            ("SF-04A-04", "Pytest scan-record persistence", "Direct proof."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-4"], e4a, manifest)

        e4b = create_epic("spiderFeet", "EPIC-SF-04B", "Stage 4b — Test nugget corpus",
                          body_template(**{"Outcome": "test_nugget_data.csv loaded."}), ["stage-4"], manifest)
        for key, title, ac in [
            ("SF-04B-01", "Generate nuggets_consumed_list.json if missing", "Distinct consumed ids."),
            ("SF-04B-02", "Author test_nugget_data.csv (AU, UK, US)", "Realistic wild values."),
            ("SF-04B-03", "Load test nuggets into spiderFeet-map", "instance_id + data set."),
            ("SF-04B-04", "Document paid/API-key-only modules", "Marked untested in map."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-4"], e4b, manifest)

        e4c = create_epic("spiderFeet", "EPIC-SF-04C", "Stage 4c — Route test execution platform",
                          body_template(**{"Outcome": "API + CLI parity for module tests."}), ["stage-4"], manifest)
        for key, title, ac in [
            ("SF-04C-01", "Module metadata refresh checklist template", "Web/API review per module."),
            ("SF-04C-02", "API: run module test from consumed nuggets", "Duration captured."),
            ("SF-04C-03", "API: persist scan-record on run", "Success/failure notes."),
            ("SF-04C-04", "API: create route after successful run", "route-state=in-test."),
            ("SF-04C-05", "API: mark service invalid when no routes work", "Per spec."),
            ("SF-04C-06", "API: module test history paged (10 rows)", "For widget table."),
            ("SF-04C-07", "Tests tab API: list route tests status aggregate", "Summary counts for UI."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-4"], e4c, manifest)

        e4mod = create_epic("spiderFeet", "EPIC-SF-04-MODULES", "Stage 4 — Module tests (177 OSINT modules)",
                            body_template(**{
                                "Problem": "Each of 177 OSINT modules must have all routes tested and recorded in spiderFeet-map.",
                                "Outcome": "One issue per module; all consumed×produced routes exercised within that issue.",
                                "Note": "Quarantine modules are out of scope until stage 5.",
                            }), ["stage-4"], manifest)
        manifest["epics"]["EPIC-SF-04-MODULES_NUM"] = e4mod

        e4w = create_epic("spiderFeet-widget", "EPIC-SFW-04", "Stage 4d — Tests tab UI",
                          body_template(**{"Outcome": "Tests page drives route execution."}), ["stage-4", "spiderFeet-widget"], manifest)
        for key, title, ac in [
            ("SFW-04-01", "Tests tab scaffold with accordions", "Grouped by module_id."),
            ("SFW-04-02", "Summary metrics table", "Route/test counts."),
            ("SFW-04-03", "Filters panel", "consumed/produced/module/grouping."),
            ("SFW-04-04", "Accordion header: run, status, duration", "Per spec."),
            ("SFW-04-05", "Accordion body: CLI/API copy buttons", "Commands with sample data."),
            ("SFW-04-06", "Accordion body: scan-record mini graph", "D3 sub-graph."),
            ("SFW-04-07", "Accordion body: results errors notes", "API payload display."),
            ("SFW-04-08", "Per-module table 10 rows/page", "Performance history."),
            ("SFW-04-09", "Exploratory review: Tests tab", "GOV-08 + persistence refresh."),
        ]:
            create_story("spiderFeet-widget", key, title, body_template(**{"Acceptance": ac}), ["stage-4", "spiderFeet-widget"], e4w, manifest)

        ex4 = create_epic("spiderFeet", "EPIC-X-04", "Stage 4 — Module test coverage sign-off",
                          body_template(**{"Outcome": "All 177 module-test issues closed or documented exception."}), ["stage-4", "cross-repo"], manifest)
        for key, title, ac in [
            ("X-04-01", "Route coverage audit report", "% tested; paid/untested explicit."),
            ("X-04-02", "Operator review: stage 4 complete", "Approval before quarantine stage."),
        ]:
            create_story("spiderFeet", key, title, body_template(**{"Acceptance": ac}), ["stage-4", "cross-repo"], ex4, manifest)

    save_manifest(manifest)
    print(f"Done. Manifest: {MANIFEST}")
    print(f"Created keys: {len(manifest['created'])} epics: {len(manifest['epics'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
