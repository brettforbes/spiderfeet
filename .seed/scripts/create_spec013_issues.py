#!/usr/bin/env python3
"""Create SPEC-013 (Projects & Composer refinement) GitHub issues across the
three repos via `gh`. Creates epic issues first, then story issues that
reference their parent epic. Writes a mapping JSON and prints markdown rows for
the issue-index docs.

Usage:
  python .seed/scripts/create_spec013_issues.py            # dry-run (prints plan)
  python .seed/scripts/create_spec013_issues.py --create   # actually create
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SPEC = ".governance/specs/SPEC-013-projects-composer-refinement.md"

REPOS = {
    "backend": "brettforbes/spiderfeet",
    "widget": "brettforbes/spiderfeet-widget",
    "yaml": "brettforbes/yaml-workflow-widget",
}
INDEX = {
    "backend": ".governance/project/SPEC013_ISSUE_INDEX.md",
    "widget": ".governance/project/SPEC013_WIDGET_ISSUE_INDEX.md",
    "yaml": ".governance/project/SPEC013_ISSUE_INDEX.md",
}

# epic code -> (repo, title, requirement span)
EPICS = [
    ("B1", "backend", "Project schema, CRUD & API alignment", "R13-01..03"),
    ("B2", "backend", "YAML\u21c4TypeDB round-trip & project lifecycle API", "R13-04..06"),
    ("B3", "backend", "Seed 5 projects + verification", "R13-07..09"),
    ("W1", "widget", "UI density pass", "R13-10"),
    ("W2", "widget", "Navbar auto-hide", "R13-11"),
    ("W3", "widget", "Projects page refinement", "R13-12..15"),
    ("W4", "widget", "Composer dropdown + Workflow Bar controls", "R13-16..18"),
    ("W5", "widget", "Widget acceptance", "R13-19"),
    ("Y1", "yaml", "Remove DAG title bar + host-driven controls", "R13-20..21"),
    ("Y2", "yaml", "Embed layout fix", "R13-22"),
    ("Y3", "yaml", "Dimensions + fit rules", "R13-23..24"),
    ("Y4", "yaml", "Zoom/pan rework + legend toggle", "R13-25..26"),
    ("Y5", "yaml", "YAML widget acceptance", "R13-27"),
]

# story code -> dict
STORIES = [
    dict(code="B1-1", epic="B1", req="R13-01", title="Schema: project entity + workflow relates project + declare project attrs",
         scope="Declare project_name/description/created attrs; finalize project as ENTITY and workflow as RELATION (relates project @card(0..1)); flip project_workflow_ids schema function.",
         deps="\u2014", verify="Schema loads on spiderfeet-actual (typedb-check/schema tx); project + workflow-links-project smoke queries succeed."),
    dict(code="B1-2", epic="B1", req="R13-02", title="Flip Python layer to entity/relation direction + project attrs",
         scope="Rewrite crud.py create/get/update/list_project (project entity; workflows link via `workflow links (project:$p)`), typedb_convert workflow forms (+project link), projections.get_project.",
         deps="B1-1", verify="Unit test create\u2192get\u2192update\u2192list project entity with 0..N linked workflows."),
    dict(code="B1-3", epic="B1", req="R13-03", title="Align project API models (no required workflow_ids)",
         scope="ProjectCreate/Update/Out expose name/description/created + optional stix; create no longer requires workflow_ids; workflow_ids derived.",
         deps="B1-2", verify="OpenAPI shows new fields; project route tests pass."),
    dict(code="B2-1", epic="B2", req="R13-04", title="Create-new-project service (project entity + info-only workflow)",
         scope="Build info-only YAML (apiVersion/kind/id/info); create project entity + workflow relation linked to project; no target/steps; NO placeholder target.",
         deps="B1-3", verify="POST then GET /projects shows new row; /complete returns info-only YAML."),
    dict(code="B2-2", epic="B2", req="R13-05", title="PUT /workflows/{id} re-parse (replace bundle)",
         scope="Accept new workflow_yaml; re-run persist_workflow_yaml(replace=True) transactionally (steps/target/edges + workflow_yaml). Invalid YAML \u2192 400, stored bundle unchanged.",
         deps="B1-3", verify="Unit test: info-only \u2192 PUT full 12A \u2192 steps/target/edges materialized; invalid YAML \u2192 400 no-mutation."),
    dict(code="B2-3", epic="B2", req="R13-06", title="GET /projects/{id}/complete (workflow_yaml inline)",
         scope="Return project attrs + linked workflow(s) with workflow_yaml inline + parsed step/target summary for one-call Composer load.",
         deps="B1-3", verify="Shape test against a seeded project; single call yields the YAML the Composer needs."),
    dict(code="B3-1", epic="B3", req="R13-07", title="Idempotent seed script for 5 projects (fully materialized, no results)",
         scope="Seed 5 projects: #1 from 12A2; #2-5 as 12A clones with fresh ids + rewritten inputs.targets.values + distinct names. persist_workflow_yaml materializes target+steps+edges; no scan results.",
         deps="B2-1,B2-2,B2-3", verify="Runs against spiderfeet-actual; then B3-2."),
    dict(code="B3-2", epic="B3", req="R13-08", title="Seed verification query (counts/edges/no-results) [OPERATOR GATE]",
         scope="Read-tx asserts 5 projects; #1 has 1 step (netdiscover) no target-input; clones have subfinder/nmap/nerva/httpx/katana/nuclei + needs edges; no scan_result_graph/results.",
         deps="B3-1", verify="Assertions pass; output recorded in issue.", gate=True),
    dict(code="B3-3", epic="B3", req="R13-09", title="pytest coverage for B1/B2 + seed smoke",
         scope="Cover B1-2/B1-3/B2-1/B2-2/B2-3 + seed smoke; poetry run pytest; bind tests to R13 IDs.",
         deps="B3-1", verify="poetry run pytest green for the new tests."),
    dict(code="W1-1", epic="W1", req="R13-10", title="Reduce navbar logo height + toolbar/content padding across panes",
         scope="Tighten navbar logo height, toolbar py, content padding across all panes; keep custom.css + custom.scss in sync.",
         deps="\u2014", verify="Visual check each pane tighter, no clipping/overlap; screenshots."),
    dict(code="W2-1", epic="W2", req="R13-11", title="Auto-hide navbar (~3s idle + on-navigate) with top-edge/keyboard reveal",
         scope="Slide navbar up after ~3s idle and on tab activate; reveal on cursor within ~48px of top or focus/Tab; respect reduced-motion; accessible; no state trap.",
         deps="\u2014", verify="Each tab: hides then reveals via hover + keyboard."),
    dict(code="W3-1", epic="W3", req="R13-12", title="Projects table columns \u2192 Name/Description/Created/Workflows/STIX",
         scope="Render columns from new ProjectOut fields (R13-03) + actions.",
         deps="B1-3", verify="Renders 5 seeded projects with names/descriptions."),
    dict(code="W3-2", epic="W3", req="R13-13", title="Resilient load: backend-unreachable state + retry",
         scope="Friendly 'Backend unreachable' panel + Retry + one auto-retry; distinguish empty vs error; drop raw NetworkError dump; document API start.",
         deps="\u2014", verify="API down \u2192 friendly state + working retry; API up \u2192 table loads."),
    dict(code="W3-3", epic="W3", req="R13-14", title="New Project modal: Name+Description editable; read-only id+created; create\u2192Composer",
         scope="Modal fields name+description; read-only generated project--<uuid> + created(now); create via R13-04 \u2192 redirect to Composer with new project loaded.",
         deps="B2-1", verify="Create \u2192 row appears (refresh proof) \u2192 Composer opens with info-only YAML."),
    dict(code="W3-4", epic="W3", req="R13-15", title="Double-click row \u2192 open in Composer via /complete",
         scope="dblclick row \u2192 GET /projects/{id}/complete \u2192 setYaml into iFrame. Single-click selects.",
         deps="B2-3", verify="Double-click loads the project's workflow into the iFrame."),
    dict(code="W4-1", epic="W4", req="R13-16", title="Composer project dropdown + 'Add new project' checkbox",
         scope="Dropdown next to project label; top item = Add-new checkbox \u2192 New Project modal; other items = projects; select \u2192 load via /complete + update label.",
         deps="W3-3,B2-3", verify="Switching projects reloads iFrame; add-new opens modal and selects new project on create."),
    dict(code="W4-2", epic="W4", req="R13-17", title="Workflow Bar pencil\u2194spectacles (edit) + gear (settings) wired to iFrame",
         scope="Pencil toggles to spectacles when editing; gear opens iFrame settings. Send setEditMode/openSettings (R13-21); reflect editModeChanged. No YAML/layout-dump buttons.",
         deps="Y1-2", verify="Pencil enters edit (\u2192 spectacles); spectacles returns read-only; gear opens settings."),
    dict(code="W4-3", epic="W4", req="R13-18", title="Persist editor YAML on edit-exit + Run Workflow (PUT /workflows/{id})",
         scope="On leaving edit mode (spectacles) and on Run Workflow, PUT latest YAML (R13-05); re-fetch to confirm persisted.",
         deps="B2-2,W4-2", verify="Edit\u2192spectacles\u2192re-fetch shows updated workflow_yaml + materialized steps; same on Run Workflow."),
    dict(code="W5-1", epic="W5", req="R13-19", title="GOV-08 exploratory review of Projects + Composer [OPERATOR GATE]",
         scope="Scenario matrix (happy/empty/loading/unreachable/create/double-click/dropdown+add-new/edit\u2192persist/navbar/density) vs live backend + 5 seeds; classify + file follow-ups.",
         deps="W3,W4", verify="Exploratory route report; all scenarios classified.", gate=True),
    dict(code="Y1-1", epic="Y1", req="R13-20", title="Remove 'CLI Workflow DAG' title bar in all modes",
         scope="Delete .dag-toolbar title bar (App.vue L7-81) in embed + standalone; preserve edit/settings state; expose via host messages + minimal on-canvas affordances.",
         deps="\u2014", verify=":4009 and :4009/?embed=1 show no title bar; app renders 12A."),
    dict(code="Y1-2", epic="Y1", req="R13-21", title="Add host messages setEditMode/openSettings/setLegendVisible + docs",
         scope="Inbound setEditMode{editing}(+editModeChanged echo), openSettings, setLegendVisible{visible}; preserve existing messages; update HOST_PROTOCOL.md.",
         deps="Y1-1", verify="postMessage smoke toggles edit/settings/legend from a host stub."),
    dict(code="Y2-1", epic="Y2", req="R13-22", title="Remove 33% embed shrink + overlays; full-bleed centered diagram",
         scope="Remove .embed .embed-diagram max-width:33.333%/margin:auto + viewport-reduction; diagram fills iframe centered; scrollbar far-right; legend anchored. Fix the 5 symptoms in .seed/18 \u00a72.2.5.",
         deps="\u2014", verify=":4009/?embed=1 full width: no empty thirds, scrollbar far right, legend correct, whole diagram reachable."),
    dict(code="Y3-1", epic="Y3", req="R13-23", title="Track DAG bbox/centre-line at 100% zoom",
         scope="Compute + store bbox at 100%: centre line, left/right widths from centre, top/bottom; recompute on layout change.",
         deps="Y2-1", verify="Dimensions match 12A/12A2 goldens."),
    dict(code="Y3-2", epic="Y3", req="R13-24", title="Default 50%/fit-to-width view + on-canvas reset",
         scope="Default 50% zoom, centered, Start at top, vertical scroll; if wider than host at 50% zoom out until L/R edges 5px inside; on-canvas reset restores default.",
         deps="Y3-1", verify="Both workflows open at default view in host partial-width + standalone."),
    dict(code="Y4-1", epic="Y4", req="R13-25", title="CTRL+/-/CTRL-wheel zoom; wheel=vertical pan; drag=pan",
         scope="CTRL+/CTRL- keys and CTRL+wheel zoom; plain wheel vertical pan (right scrollbar); click-drag pan both axes; clamps compatible with fit rules.",
         deps="Y3-2", verify="Each input behaves as specified; no accidental zoom on plain wheel."),
    dict(code="Y4-2", epic="Y4", req="R13-26", title="Settings 'Show legend' toggle + host setLegendVisible",
         scope="Add Show-legend checkbox (default on) wrapping EdgeLegend; also driven by host message; keep theme + coloured-edges.",
         deps="Y1-2", verify="Toggling hides/shows legend from settings and host message."),
    dict(code="Y5-1", epic="Y5", req="R13-27", title="Smoke + visual verification on 12A/12A2 (embed + standalone) [OPERATOR GATE]",
         scope="Verify: no title bar; full-bleed embed; default 50%/fit view; CTRL zoom + wheel/drag pan; host edit/settings/legend messages. Screenshots attached.",
         deps="Y1,Y2,Y3,Y4", verify="Screenshots + smoke recorded.", gate=True),
]


def gh_create(repo: str, title: str, body: str) -> str:
    out = subprocess.run(
        ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"gh failed for {title!r}: {out.stderr.strip()}")
    url = out.stdout.strip().splitlines()[-1]
    return url


def num_from_url(url: str) -> int:
    m = re.search(r"/issues/(\d+)", url)
    return int(m.group(1)) if m else -1


def epic_body(code: str, name: str, span: str, repo_key: str) -> str:
    return (
        f"Epic **{code}** for SPEC-013 (Projects & Composer refinement).\n\n"
        f"- Spec: `{SPEC}` (in `spiderfeet`)\n"
        f"- Issue index: `{INDEX[repo_key]}` \u2192 section `{code}`\n"
        f"- Requirements: {span}\n\n"
        "Child stories are linked below after creation. Governance: sequential, "
        "one child at a time \u2014 branch from `develop` \u2192 PR \u2192 close with completion note \u2192 "
        "merge before the next. Autonomous self-merge for non-gate stories; stop at operator gates."
    )


def story_body(s: dict, epic_num: int, repo_key: str) -> str:
    gate = " **[OPERATOR GATE \u2014 do not self-merge; hand to operator]**" if s.get("gate") else ""
    return (
        f"Parent epic: #{epic_num}{gate}\n\n"
        f"- Requirement: **{s['req']}** \u00b7 Spec `{SPEC}`\n"
        f"- Full detail: `{INDEX[repo_key]}` \u2192 \"{s['code']}\"\n\n"
        f"## Scope\n{s['scope']}\n\n"
        f"## Depends on\n{s['deps']}\n\n"
        f"## Verify\n{s['verify']}\n\n"
        "## Governance\nBranch `feature/<n>-<slug>` from `develop` \u2192 smallest coherent change \u2192 "
        "verify \u2192 PR into `develop` \u2192 close this issue with a completion note (what changed + evidence) "
        "\u2192 merge before the next issue. TypeDB/schema work follows `.cursor/skills/typedb/SKILL.md`."
    )


def main() -> None:
    create = "--create" in sys.argv
    mapping: dict[str, dict] = {}

    # Epics first
    epic_num: dict[str, int] = {}
    for code, repo_key, name, span in EPICS:
        repo = REPOS[repo_key]
        title = f"[SPEC-013] {code} \u2014 {name}"
        body = epic_body(code, name, span, repo_key)
        if create:
            url = gh_create(repo, title, body)
            n = num_from_url(url)
        else:
            url, n = f"(dry-run {repo})", -1
        epic_num[code] = n
        mapping[code] = dict(repo=repo, kind="epic", title=title, number=n, url=url)
        print(f"EPIC {code:3} {repo_key:7} #{n} {url}")

    # Stories
    for s in STORIES:
        repo_key = next(rk for c, rk, *_ in EPICS if c == s["epic"])
        repo = REPOS[repo_key]
        title = f"[SPEC-013] {s['code']} \u2014 {s['title']}"
        body = story_body(s, epic_num.get(s["epic"], -1), repo_key)
        if create:
            url = gh_create(repo, title, body)
            n = num_from_url(url)
        else:
            url, n = f"(dry-run {repo})", -1
        mapping[s["code"]] = dict(repo=repo, kind="story", epic=s["epic"], title=title, number=n, url=url)
        print(f"  {s['code']:5} {repo_key:7} #{n} {url}")

    outp = Path(".seed/scripts/spec013_issue_map.json")
    outp.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"\nWrote {outp} ({len(mapping)} issues). create={create}")


if __name__ == "__main__":
    main()
