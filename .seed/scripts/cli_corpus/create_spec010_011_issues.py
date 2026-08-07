#!/usr/bin/env python3
"""Create SPEC-010 (spiderfeet) + SPEC-011 (spiderfeet-widget) epics & stories via gh CLI.

Idempotency: this creates NEW issues each run. Use --dry-run first to review titles.

Usage:
  python .seed/scripts/cli_corpus/create_spec010_011_issues.py --dry-run
  python .seed/scripts/cli_corpus/create_spec010_011_issues.py            # real run
  python .seed/scripts/cli_corpus/create_spec010_011_issues.py --spec 010 # one spec only

Side effects (real run):
  - ensures labels `story`, `spec-010` (spiderfeet) / `spec-011` (widget) exist
  - creates epics (labels: epic, enhancement, spec-0xx) + stories (labels: story, enhancement, spec-0xx)
  - links each story as a GitHub sub-issue of its epic
  - adds every created issue to user Project board #1
  - rewrites the two ISSUE_INDEX.md files with real issue numbers
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # C:/projects/spiderfeet
WIDGET_ROOT = ROOT.parent / "spiderfeet-widget"
PROJECT_OWNER = "brettforbes"
PROJECT_NUMBER = "1"

REPO_BACKEND = "brettforbes/spiderfeet"
REPO_WIDGET = "brettforbes/spiderfeet-widget"

DRY = False


def run(cmd: list[str], check: bool = True) -> str:
    if DRY:
        print("DRY:", " ".join(cmd))
        return ""
    return subprocess.run(cmd, text=True, capture_output=True, check=check).stdout.strip()


def ensure_label(repo: str, name: str, color: str, desc: str) -> None:
    subprocess.run(
        ["gh", "label", "create", name, "--repo", repo, "--color", color,
         "--description", desc, "--force"],
        text=True, capture_output=True, check=False,
    )


def gh_create(repo: str, title: str, body: str, labels: list[str]) -> dict:
    if DRY:
        print(f"DRY create [{repo}] {title}  labels={labels}")
        return {"number": 0, "url": "", "id": 0}
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fh:
        fh.write(body.strip() + "\n")
        path = fh.name
    cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body-file", path]
    for lab in labels:
        cmd.extend(["--label", lab])
    url = subprocess.check_output(cmd, text=True).strip()
    Path(path).unlink(missing_ok=True)
    number = int(url.rstrip("/").split("/")[-1])
    dbid = int(subprocess.check_output(
        ["gh", "api", f"repos/{repo}/issues/{number}", "--jq", ".id"], text=True).strip())
    add_to_project(url)
    print(f"  [{repo}] #{number}  {title}")
    return {"number": number, "url": url, "id": dbid}


def add_to_project(url: str) -> None:
    if DRY or not url:
        return
    subprocess.run(
        ["gh", "project", "item-add", PROJECT_NUMBER, "--owner", PROJECT_OWNER, "--url", url],
        text=True, capture_output=True, check=False,
    )


def link_sub_issue(repo: str, parent_number: int, child_dbid: int) -> None:
    if DRY:
        print(f"DRY sub-issue link [{repo}] parent#{parent_number} <- child_id {child_dbid}")
        return
    subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{repo}/issues/{parent_number}/sub_issues",
         "-F", f"sub_issue_id={child_dbid}"],
        text=True, capture_output=True, check=False,
    )


# ---------------------------------------------------------------------------
# Footers
# ---------------------------------------------------------------------------

def footer(spec: str, plan_path: str, spec_path: str, forbidden: list[str]) -> str:
    forb = "\n".join(f"- {f}" for f in forbidden)
    return f"""
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Autonomous execution (no human review wait required)
Operator has pre-authorized fully autonomous execution for {spec} (see `{plan_path}` §0).
Implement -> verify -> comment evidence -> PR -> **self-merge via `gh pr merge --squash --delete-branch`** ->
close this issue with a comment linking the PR + evidence -> update the issue index -> return to
`develop` -> pick the next unblocked child. The only exceptions are the operator gates noted in the plan §0.1.

## Forbidden ({spec})
{forb}

## Agent instructions
1. Read `{plan_path}` for this story's epic section (full scope + verify commands).
2. Read the {spec} requirement IDs cited above in `{spec_path}`.
3. One issue -> one PR -> self-merge -> comment verification evidence -> close issue -> update index.
"""


FORBIDDEN_010 = [
    "Do not leave any literal `IP_ADDRESS` in emitting/matching code after Epic AH",
    "Do not import from `.seed/scripts/cli_corpus/*` inside `modules_v2/` (port must be self-contained)",
    "Do not delete the original `.seed/scripts/cli_corpus/` tree",
    "Do not add a `typedb-bridge` dependency — `typedb-driver` directly",
    "Do not build a shell-string command path — argv arrays only",
    "Do not touch production v1 `sfp_*` OSINT modules or the `sfp-api-*` catalogue",
    "Do not break widget-consumed v1 routes when absorbing them",
    "Do not mark a scan module done while an output form is text-native where a structured mode exists",
]
FORBIDDEN_011 = [
    "Do not modify the `yaml-workflow-widget` repo; integrate via its postMessage contract only",
    "Do not hand-roll `postMessage` for the Data Viewer / structured pane — use `DataViewerHost`",
    "Do not duplicate `CliScanApp` or `CanvasGraph`; reuse and extend minimally",
    "Do not store `temporary_id` on the server — strip before send",
    "Do not break Maps/Tests/Subscriptions/CLI-Profiling/Settings when renaming Enrichments->Projects",
    "Do not let the Project Context Viewer error on empty data (it is intentionally empty this spec)",
]

FOOTER_010 = footer(
    "SPEC-010",
    ".governance/project/SPEC010_AGENT_PLAN.md",
    ".governance/specs/SPEC-010-spiderfeet-v2-engine.md",
    FORBIDDEN_010,
)
FOOTER_011 = footer(
    "SPEC-011",
    ".governance/project/SPEC011_AGENT_PLAN.md",
    "@spiderfeet/.governance/specs/SPEC-011-composer-projects-ui.md",
    FORBIDDEN_011,
)


def epic_body(spec: str, problem: str, spec_ids: str, children: list[str], success: str, foot: str) -> str:
    kids = "\n".join(f"- {c}" for c in children)
    return f"""## Problem
{problem}

## Spec binding
{spec} {spec_ids}

## Children (order)
{kids}

## Success
{success}
{foot}
"""


def child_body(spec: str, code: str, parent: int, spec_ids: str, spec_path_ref: str,
               outcome: str, scope: str, verify: str, blocked_by: str, gate: str, foot: str) -> str:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    gate_s = f"\n## Hard gate\n{gate}\n" if gate else ""
    return f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Desired outcome
{outcome}

## Spec binding
{spec} {spec_ids} · Parent epic #{parent} · Spec `{spec_path_ref}`

## Scope
{scope}
{blocked}{gate_s}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in PR/issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue
- [ ] Matching epic section of the agent plan followed

## Verification
{verify}
{foot}
"""


# ---------------------------------------------------------------------------
# SPEC-010 data (backend)
# ---------------------------------------------------------------------------

SPEC010_SPECPATH = ".governance/specs/SPEC-010-spiderfeet-v2-engine.md"

EPICS_010 = {
    "AH": ("Epic AH - IP_ADDRESS -> IPV4/IPV6 disambiguation (prerequisite)",
           "The ambiguous `IP_ADDRESS` nugget is used throughout the CLI-profiling stack. Split it into unambiguous `IPV4_ADDRESS`/`IPV6_ADDRESS`, driven by the centralized address parser (`core/ip_classify.py`), across code, rules, catalogues, schema, docs, and regenerated artifacts. Prerequisite for all v2 engine work.",
           "R10-01, R10-02, R10-03, R10-04, R10-05",
           ["AH0 Migration inventory", "AH1 Catalogue split", "AH2 Rules + code",
            "AH3 Schema + structure docs + proj-07", "AH4 Regenerate + re-verify artifacts"],
           "No non-legacy `IP_ADDRESS` remains anywhere in the profiling stack; every address node is `IPV4_ADDRESS` or `IPV6_ADDRESS`; all affected artifacts regenerated and verified."),
    "AI": ("Epic AI - Schema reconcile + spiderfeet-actual load",
           "The v2 TypeDB schema has reconcilable gaps vs the corpus graph JSON (edge naming, missing `scan_step relates produced`) and no DB load path. Reconcile and load into a fresh `spiderfeet-actual`.",
           "R10-06, R10-07, R10-08, R10-09",
           ["AI0 Edge-naming mapping doc", "AI1 relates produced", "AI2 fun JSON projections",
            "AI3 Bootstrap load spiderfeet-actual [G1]"],
           "`spiderfeet-actual` loads cleanly from the reconciled schema with the 8 CLI services seeded; `fun` queries return JSON-ready projections."),
    "AJ": ("Epic AJ - Port CLI-corpus engine into modules_v2/_core",
           "Port the production corpus engine + rules into a self-contained `modules_v2/_core` + `_rules` so v2 modules do not import from `.seed/scripts/cli_corpus`. Add the v2 typedb-driver client.",
           "R10-10, R10-11, R10-12, R10-13",
           ["AJ1 Port _core engines", "AJ2 Port _rules + catalogues", "AJ3 typedb-driver client",
            "AJ4 Parity harness"],
           "`modules_v2` is self-contained; ported engine produces parity output for all 8 tools; v2 DB client connects to `spiderfeet-actual`."),
    "AK": ("Epic AK - Eight v2 CLI modules (four-output)",
           "Implement the v2 module contract and real four-output modules for all 8 tools using `_core`, replacing the incomplete nmap stub.",
           "R10-14, R10-15, R10-16",
           ["AK0 _base + nmap rewrite", "AK1 netdiscover", "AK2 nerva", "AK3 pius",
            "AK4 subfinder", "AK5 httpx", "AK6 katana", "AK7 nuclei"],
           "All 8 `sfp_cli_<tool>.py` import clean and produce Text/Structured/Graph/Narrative from live scans, structured-first."),
    "AL": ("Epic AL - TypeDB persistence + JSON projections",
           "CRUD + dual-form subgraph persistence (json-string + in-graph) + JSON projection functions over the AI2 `fun` queries.",
           "R10-17, R10-18, R10-19",
           ["AL1 Entity CRUD", "AL2 Dual-form subgraph serializer", "AL3 JSON projection functions"],
           "Project/workflow/target/scan_step/subgraph round-trip to/from JSON; scan_step round-trips its four forms + consumed/produced nuggets losslessly."),
    "AM": ("Epic AM - Workflow DSL + GSE runtime",
           "Integrate the SPEC-007 workflow DSL + GSE evaluation into spiderfeet_v2: validate, schedule the needs-DAG, resolve inputs, evaluate output.vars, YAML<->TypeDB conversion, and context export/merge.",
           "R10-20, R10-21, R10-22",
           ["AM1 Parse/validate/schedule + GSE", "AM2 YAML<->TypeDB conversion", "AM3 Context export + merge"],
           "The 12A workflow validates + schedules; workflows convert both directions; scan_graph export + append-unique temporary-context merge work."),
    "AN": ("Epic AN - FastAPI v2 app (absorb v1 + new routes)",
           "Make spiderfeet_v2 the app on 127.0.0.1:8001, absorbing the v1 routers the widget consumes and adding the new v2 project/workflow/scan/context routes.",
           "R10-23, R10-24, R10-25, R10-26",
           ["AN1 Absorb v1 + serve on 8001 [G2]", "AN2 New v2 routes", "AN3 Route tests + v1 regression"],
           "8001 serves both the unchanged v1 routes (Maps/Tests/Subscriptions/CLI-Profiling/content) and the new v2 endpoints, all tested."),
    "AO": ("Epic AO - Workflow orchestrator",
           "Run a workflow step (module -> four forms -> persist -> output vars -> export) and chain a full workflow by needs.",
           "R10-27, R10-28",
           ["AO1 Single-step run", "AO2 Full-workflow chaining"],
           "The 12A split-branch workflow chains end-to-end on a lab target, persisting scan_steps and accumulating the temporary context."),
    "AP": ("Epic AP - Backend end-to-end acceptance (4 targets)",
           "Run the 12A workflow live against the 4 example targets and provide a reproducible acceptance script.",
           "R10-29, R10-30",
           ["AP1 4-target live run [G3]", "AP2 Acceptance script"],
           "Live 4-target run signed off by the operator; acceptance script asserts no IP_ADDRESS nodes, no orphans, four-form storage, queryable JSON."),
}

# (code, title, spec_ids, epic, outcome, scope, verify, blocked_by, gate)
STORIES_010 = [
    ("AH0", "Migration inventory", "R10-01", "AH",
     "A complete inventory of every IP_ADDRESS occurrence with a migrate/keep/regen classification.",
     "Produce `.governance/project/SPEC010_IP_MIGRATION_INVENTORY.md` covering cli_corpus, nuggets*.json, the v2 .tql, docs-for-cli-tools, content bundles, and generated artifacts; classify each occurrence.",
     "Inventory checked in; its grep counts match a fresh `rg -c IP_ADDRESS`.", "", ""),
    ("AH1", "Catalogue split", "R10-02", "AH",
     "IPV4_ADDRESS and IPV6_ADDRESS exist in the catalogue; derived *_IPADDR variants audited.",
     "Add IPV4_ADDRESS + IPV6_ADDRESS to `nuggets_extension.json`; audit AFFILIATE/BLACKLISTED/MALICIOUS IPADDR variants per the inventory.",
     "`nuggets_extension.json` contains both new ids with type ENTITY, colour, description.", "AH0", ""),
    ("AH2", "Rules + adapter/topology/correlation code", "R10-03", "AH",
     "All emitting/matching code produces IPV4/IPV6 only, via classify_ip.",
     "Update `rules/_shared/ip_patterns.yaml` + `core/ip_classify.py` (host IPv4 -> IPV4_ADDRESS), all 8 `rules/<tool>/*.yaml`, and topology/correlation/adapters.",
     "`rg IP_ADDRESS .seed/scripts/cli_corpus` returns only inventory keep-legacy lines.", "AH1", ""),
    ("AH3", "Schema + structure docs + proj-07", "R10-04", "AH",
     "Schema + docs + rule doc consistently use ipv4/ipv6.",
     "Reconcile `.seed/spiderfeet_v2_semantic.tql` to ipv4-address/ipv6-address; update nugget_structure docs, `_Current_Ontology.md`, and the proj-07 IP-addresses table.",
     "Schema parses; docs + proj-07 grep show the split.", "AH2", ""),
    ("AH4", "Regenerate + re-verify artifacts", "R10-05", "AH",
     "All affected artifacts regenerated with correct IP classification, no orphans.",
     "Regenerate graph JSON + narrative MD via `backfill_adapter_four_outputs.py` for all 8 tools; refresh content graph_structure.md; re-run graph validation.",
     "Backfill runs for all 8; repo-wide `rg IP_ADDRESS` matches only keep-legacy.", "AH3", ""),

    ("AI0", "Edge-naming mapping doc", "R10-06", "AI",
     "One canonical had/contains/listens-to <-> has_this/contains_this/listens_to_this mapping documented.",
     "Write a short design note fixing the graph-JSON<->TypeQL relation mapping (both directions) and reconciling the seed §3.2 example.",
     "Note checked in; mapping table complete for all three relations both directions.", "", ""),
    ("AI1", "relates produced", "R10-07", "AI",
     "scan_step round-trips produced nuggets.",
     "Add `scan_step relates produced @card(0..)`; confirm `nugget plays scan_step:produced` round-trips.",
     "Schema parses; a define+insert+match smoke reads back a produced nugget.", "AI0", ""),
    ("AI2", "fun JSON projections", "R10-08", "AI",
     "fun queries return JSON-ready projections for project/workflow/scan_step + extended contains_recursive.",
     "Write the fun queries (project, workflow, scan_step, contains_recursive incl. had/listens-to).",
     "typedb skill: each fun runs against a seeded fixture and covers the documented fields.", "AI1", ""),
    ("AI3", "Bootstrap load spiderfeet-actual", "R10-09", "AI",
     "spiderfeet-actual loads from the reconciled schema with the 8 services seeded.",
     "`spiderfeet_v2/db/bootstrap` loads `.tql` into a fresh `spiderfeet-actual` and seeds the 8 sfp-cli-app-* services; `--reset` idempotent.",
     "After G1 approval: `python -m spiderfeet_v2.db.bootstrap --reset` then a read confirms schema + 8 services.",
     "AH4, AI2",
     "**G1 OPERATOR GATE.** Loading/resetting `spiderfeet-actual` is destructive. Post the exact command + a no-data-loss confirmation and wait for an operator approval comment on THIS issue before running it."),

    ("AJ1", "Port _core engines", "R10-10", "AJ",
     "modules_v2/_core is a self-contained copy of the corpus engine.",
     "Copy cli_corpus/core/* into `modules_v2/_core/` with imports rewritten to `modules_v2._core.*`; include narrative_report.",
     "`python -c 'import modules_v2._core'` clean; `rg cli_corpus modules_v2` returns nothing.", "", ""),
    ("AJ2", "Port _rules + catalogues", "R10-11", "AJ",
     "Rule packs + catalogues load from within modules_v2.",
     "Copy rule packs to `modules_v2/_rules/`; make _core resolve them + load nuggets*.json from a configurable path under modules_v2.",
     "_core loads all rule packs + catalogues without reaching outside modules_v2.", "AJ1", ""),
    ("AJ3", "typedb-driver client", "R10-13", "AJ",
     "spiderfeet_v2/db connects to spiderfeet-actual via typedb-driver.",
     "`spiderfeet_v2/db/connection.py` + `config.py` mirroring spiderfeet/map/, targeting spiderfeet-actual; no typedb-bridge.",
     "`python -m spiderfeet_v2.db --ping-only` connects or reports clearly.", "", ""),
    ("AJ4", "Parity harness", "R10-12", "AJ",
     "Ported engine matches original corpus output for all 8 tools (incl. IPv4/IPv6 split).",
     "For each tool, run ported _core over a recorded structured fixture and diff graph+narrative vs original cli_corpus output; document explained diffs.",
     "`pytest modules_v2/_core/tests/test_parity.py -q` green for all 8.", "AJ2", ""),

    ("AK0", "_base contract + nmap rewrite", "R10-14", "AK",
     "The v2 four-output module contract exists; nmap is real, import-clean four-output code.",
     "`modules_v2/_base.py` (four-output run()); rewrite `sfp_cli_nmap.py` to real code using _base+_core; fix its syntax errors.",
     "`python -c 'import modules_v2.sfp_cli_nmap'` clean; nmap live smoke on scanme.nmap.org yields four forms.", "AJ4", ""),
    ("AK1", "sfp_cli_netdiscover", "R10-15, R10-16", "AK",
     "netdiscover v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_netdiscover.py` per _base via _core, structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK2", "sfp_cli_nerva", "R10-15, R10-16", "AK",
     "nerva v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_nerva.py` per _base via _core (JSONL bundle + correlation), structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK3", "sfp_cli_pius", "R10-15, R10-16", "AK",
     "pius v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_pius.py` per _base via _core (NDJSON), structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK4", "sfp_cli_subfinder", "R10-15, R10-16", "AK",
     "subfinder v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_subfinder.py` per _base via _core (JSONL), structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK5", "sfp_cli_httpx", "R10-15, R10-16", "AK",
     "httpx v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_httpx.py` per _base via _core (JSONL), structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK6", "sfp_cli_katana", "R10-15, R10-16", "AK",
     "katana v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_katana.py` per _base via _core (JSONL), structured-first.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),
    ("AK7", "sfp_cli_nuclei", "R10-15, R10-16", "AK",
     "nuclei v2 module produces four forms from a live run.",
     "Implement `modules_v2/sfp_cli_nuclei.py` per _base via _core (JSONL), structured-first; follow nuclei_strategy skill.",
     "Import-clean; live smoke; four forms; no orphan/IP_ADDRESS nodes.", "AK0", ""),

    ("AL1", "Entity CRUD", "R10-17", "AL",
     "project/workflow/target/scan_step/subgraph CRUD round-trips to/from JSON.",
     "Implement CRUD in `spiderfeet_v2/db/` for all entity/relation types, each <-> JSON.",
     "`pytest spiderfeet_v2/db/tests/test_crud.py -q` against a scratch DB.", "AI3, AJ3", ""),
    ("AL2", "Dual-form subgraph serializer", "R10-18", "AL",
     "Subgraphs persist as both json-string and in-graph forms via one serializer.",
     "One serializer/deserializer bridging graph JSON <-> TypeDB in-graph form (using the AI0 edge mapping), storing both forms.",
     "Round-trip test: JSON graph -> store (both) -> read back -> equal.", "AL1, AI0", ""),
    ("AL3", "JSON projection functions", "R10-19", "AL",
     "Python wrappers over fun queries return project/workflow/scan_step JSON.",
     "Wrap the AI2 fun queries; scan_step round-trips its four UI forms + consumed/produced nuggets losslessly.",
     "`pytest spiderfeet_v2/db/tests/test_projections.py -q`.", "AL2, AI2", ""),

    ("AM1", "Parse/validate/schedule + GSE", "R10-20", "AM",
     "Workflow YAML validates + schedules; GSE evaluates output.vars.",
     "Integrate `.seed/scripts/cli_workflow/` into `spiderfeet_v2/workflow/`: validate vs schemas, schedule needs-DAG, resolve input.from, build argv/files, evaluate output.vars GSE.",
     "`pytest spiderfeet_v2/workflow/tests/test_dsl.py -q` incl. the 12A example.", "AJ4", ""),
    ("AM2", "YAML <-> TypeDB conversion", "R10-21", "AM",
     "Workflows convert both directions consistently.",
     "Convert workflow TypeDB form (+ *_yaml attrs) <-> YAML-DSL/JSON.",
     "Round-trip: YAML -> TypeDB -> YAML equals canonical; TypeDB -> JSON matches API shape.", "AM1, AL1", ""),
    ("AM3", "Context export + merge", "R10-22", "AM",
     "scan_graph export marks graphs; append-unique temporary-context merge.",
     "`context.export: scan_graph` marks a scan_result_graph for export; append-unique merge (nodes by id, edges by (source,target,relation)).",
     "Test merging two overlapping scan graphs yields deduped nodes/edges.", "AM1, AL2", ""),

    ("AN1", "Absorb v1 + serve on 8001", "R10-23", "AN",
     "spiderfeet_v2 becomes the 8001 app; absorbed v1 routes unchanged.",
     "`spiderfeet_v2/api/` mounts the v1 routers (map/tests/subscriptions/cli-corpus/content) and serves 8001; CORS retained.",
     "After G2 approval: start v2 app; curl each absorbed route returns the same shape; regression pytest green.",
     "AL1, AM1",
     "**G2 OPERATOR GATE.** The 8001 cutover changes what the running widget talks to. Land behind an operator approval comment on THIS issue, with evidence the absorbed v1 routes respond identically. Until approved, run the v2 app on a scratch port."),
    ("AN2", "New v2 routes", "R10-24, R10-25", "AN",
     "projects/workflows/targets CRUD, execute, scan_step, contexts (with temporary-id stripping) live.",
     "Implement the new v2 routes incl. temporary-context update that strips temporary_id and remaps edges to nugget_instance_id; Pydantic + OpenAPI examples.",
     "`pytest spiderfeet_v2/api/tests/test_v2_routes.py -q`; /docs shows examples.", "AN1, AL3, AM2", ""),
    ("AN3", "Route tests + v1 regression", "R10-26", "AN",
     "New routes tested; absorbed v1 routes proven unaffected.",
     "pytest for all new routes + regression proving absorbed v1 routes unchanged.",
     "Full API suite green.", "AN2", ""),

    ("AO1", "Single-step run", "R10-27", "AO",
     "One workflow step runs module -> four forms -> persist -> output vars -> export.",
     "Orchestrator: resolve inputs -> invoke module (AK) -> capture four forms -> persist scan_step + scan_result_graph -> eval output.vars -> export when scan_graph. Record status lifecycle.",
     "Run one subfinder step live; scan_step persisted with four forms; output vars populated.", "AK0, AL2, AM3", ""),
    ("AO2", "Full-workflow chaining", "R10-28", "AO",
     "A full workflow chains by needs, threading output vars and accumulating exported graphs.",
     "Chain steps by needs; thread prior output vars into later input.from; accumulate exported graphs into the project temporary context.",
     "Run 12A on a lab/permissive target; all steps persist; temporary context accumulates.", "AO1", ""),

    ("AP1", "4-target live run", "R10-29", "AP",
     "12A runs live against the 4 example targets with a recorded evidence bundle.",
     "Run 12A end-to-end against sbs.com.au, k2am.com.au, venturecapitalopportunitiesfund.com.au, squarepeg.vc; capture per-step four forms, persisted subgraphs, temporary-context contributions.",
     "Evidence bundle under `spiderfeet_v2/acceptance/`; operator approval comment on THIS issue.",
     "AN3, AO2",
     "**G3 OPERATOR GATE.** Present the live 4-target acceptance run for operator sign-off; do not mark the SPEC-010 program done without an operator approval comment on THIS issue."),
    ("AP2", "Acceptance script", "R10-30", "AP",
     "A reproducible script validates the acceptance invariants.",
     "`spiderfeet_v2/acceptance/run_four_targets.py` reproduces the run and asserts: no IP_ADDRESS nodes, no orphans, four-form storage, queryable project/workflow/step/context JSON via API.",
     "`python spiderfeet_v2/acceptance/run_four_targets.py --target <one>` passes assertions.", "AP1", ""),
]

# ---------------------------------------------------------------------------
# SPEC-011 data (widget)
# ---------------------------------------------------------------------------

SPEC011_SPECPATH = "@spiderfeet/.governance/specs/SPEC-011-composer-projects-ui.md"

EPICS_011 = {
    "AQ": ("Epic AQ - v2 API client + Projects page",
           "Add a v2 engine API client and replace the disabled Enrichments nav stub with a real Projects page (renamed) backed by the SPEC-010 API.",
           "R11-01, R11-02, R11-03, R11-04, R11-05",
           ["AQ1 v2 API client", "AQ2 Rename Enrichments->Projects + pane", "AQ3 Projects table",
            "AQ4 Project CRUD + row->Composer"],
           "Projects tab lists projects with working create/edit/delete; clicking a row opens the Composer with that project loaded."),
    "AR": ("Epic AR - Composer page shell",
           "Build the Composer 4-pane layout: split central Project Context / Temporary Subgraph viewers (CanvasGraph), collapsible left column, right slide-in region, with per-pane full-screen.",
           "R11-06, R11-07, R11-08",
           ["AR1 Composer pane + layout", "AR2 Pane full-screen expand/revert", "AR3 Two CanvasGraph viewers (empty Project Context)"],
           "Composer renders the 4-pane layout; both central panes host CanvasGraph; the Project Context Viewer is empty without error; panes expand/revert."),
    "AS": ("Epic AS - Embed YAML Workflow Editor iframe",
           "Embed the yaml-workflow-widget iframe in a collapsing left column with 0/3/12-column states, the ready/setYaml/getYaml handshake, and theme sync.",
           "R11-09, R11-10, R11-11",
           ["AS1 Collapsing left iframe + width states", "AS2 Handshake + load workflow YAML", "AS3 Theme sync"],
           "The embedded editor shows the workflow diagram, collapses to 0/3/12 columns, and stays theme-matched with the host."),
    "AT": ("Epic AT - Step selection -> CliScanApp slide-in",
           "On stepSelected, slide in the correct tool's CliScanApp over columns 4-12; gate unset steps to the Scan tab with Scan Now disabled.",
           "R11-12, R11-13",
           ["AT1 stepSelected -> right slide-in per tool", "AT2 Unset-step gating"],
           "Selecting a workflow step opens its tool's 5-tab app; unset steps allow option editing with Scan Now disabled and other tabs locked."),
    "AU": ("Epic AU - Option-edit round-trip + run gating",
           "Send CliScanApp option changes back to the editor to update the workflow YAML, and enable Scan Now only when the step's YAML validates.",
           "R11-14, R11-15",
           ["AU1 Option change -> YAML update", "AU2 Validation -> enable Scan Now"],
           "Changing an option updates the editor YAML + diagram; Scan Now enables only on validationResult.ok for that step."),
    "AV": ("Epic AV - Live execute + read-only replay",
           "Wire Scan Now to the SPEC-010 execute endpoint (four forms + persistence) and replay stored runs read-only.",
           "R11-16, R11-17",
           ["AV1 Scan Now -> execute -> four forms", "AV2 Read-only replay"],
           "Running a step populates Text/Structured/Graph/Report and persists; re-opening a completed step shows its four forms read-only."),
    "AW": ("Epic AW - Temporary Subgraph Viewer behavior",
           "Import exported scan graphs with temporary_ids as discrete subgraphs, allow removal, and strip temporary_ids when sending back to the server.",
           "R11-18, R11-19, R11-20",
           ["AW1 Import with temporary_id", "AW2 Discrete render + remove toggle", "AW3 Strip-on-send round-trip"],
           "Exported scan graphs accumulate as independent subgraphs (no id collision), can be removed, and round-trip to the server with temporary_id stripped."),
    "AX": ("Epic AX - Widget end-to-end acceptance",
           "Demonstrate the full Composer flow live against the v2 engine and run a GOV-08 exploratory review.",
           "R11-21, R11-22",
           ["AX1 Live E2E [OPERATOR SIGN-OFF]", "AX2 GOV-08 exploratory review"],
           "Full Composer flow works live for a real target (operator signed off); GOV-08 review checked in with a completeness label."),
}

STORIES_011 = [
    ("AQ1", "v2 API client", "R11-01", "AQ",
     "A widget API client wraps the SPEC-010 v2 routes with UI-visible error states.",
     "`src/js/spiderfeet-api.js` wrapping projects/workflows/targets CRUD, execute, contexts against data-api-base; register in webpack widget.js order; restart npm start.",
     "Console `Widgets.SpiderfeetApi.listProjects()` returns data or a clean error against the v2 engine (or documented stub).", "", ""),
    ("AQ2", "Rename Enrichments->Projects + pane", "R11-02", "AQ",
     "The Enrichments nav becomes an enabled Projects tab with a real pane.",
     "Rename the Enrichments nav button to Projects, enable it, add `#pane-projects`, wire shell.js; leave other tabs untouched.",
     "Nav shows Projects; clicking activates #pane-projects; other tabs still work.", "", ""),
    ("AQ3", "Projects table", "R11-03", "AQ",
     "The Projects page lists projects from GET /projects with empty/loading/error states.",
     "`src/js/projects.js` renders id/created/workflow-count/stix-id; handle empty/loading/error.",
     "Table renders live data; empty and error states shown when API is empty/down.", "AQ1, AQ2", ""),
    ("AQ4", "Project CRUD + row->Composer", "R11-04, R11-05", "AQ",
     "Create/edit/delete work (verified by refresh); row click opens Composer with the project.",
     "Wire CRUD to the API (delete verified by refresh); row click fetches full project JSON and navigates to Composer (re-fetchable on refresh).",
     "Create appears after refresh; delete gone after refresh; row click lands on Composer with the right project.", "AQ3", ""),

    ("AR1", "Composer pane + layout", "R11-06", "AR",
     "The Composer tab renders the 4-region layout.",
     "Enable the Composer nav; add `#pane-composer`; build central horizontal split + collapsible left column + right slide-in region; 12-column model.",
     "Composer activates; split panes + placeholder regions render at :4001.", "AQ2", ""),
    ("AR2", "Pane full-screen expand/revert", "R11-07", "AR",
     "Each central pane can expand to full-screen and revert, keyboard-accessible.",
     "Add expand icon (top-right) + revert icon on both central panes.",
     "Expand/revert works for both panes via mouse and keyboard.", "AR1", ""),
    ("AR3", "Two CanvasGraph viewers (empty Project Context)", "R11-08", "AR",
     "Both central panes host CanvasGraph; Project Context Viewer is empty without error.",
     "Mount Viz.CanvasGraph in both panes; init Project Context Viewer with {nodes:[],links:[]}.",
     "Both canvases mount; empty Project Context Viewer renders without error.", "AR1", ""),

    ("AS1", "Collapsing left iframe + width states", "R11-09", "AS",
     "The left column embeds the editor iframe with 0/3/12-column states.",
     "`src/js/composer-workflow.js` embeds http://localhost:4009/?embed=1; three width states toggled by icons; default partial.",
     "Iframe loads; collapse/partial/full transitions work.", "AR1", ""),
    ("AS2", "Handshake + load workflow YAML", "R11-10", "AS",
     "The host loads the workflow YAML into the editor per HOST_PROTOCOL.",
     "Wait for ready, then setTheme + setYaml (current workflow YAML); listen for yamlChanged/validationResult.",
     "Editor shows the loaded diagram; validationResult received; yamlChanged observed on edit.", "AS1", ""),
    ("AS3", "Theme sync", "R11-11", "AS",
     "Host and editor stay theme-synced both ways.",
     "Widgets.Theme -> setTheme; respect iframe themeChanged; host toggle re-themes the editor.",
     "Host light/dark toggle re-themes the embedded editor both ways.", "AS2", ""),

    ("AT1", "stepSelected -> right slide-in per tool", "R11-12", "AT",
     "Selecting a step slides in the matching tool's CliScanApp over cols 4-12.",
     "On stepSelected {stepId}, resolve the tool from the step's uses and slide in that CliScanApp; handle special step ids gracefully.",
     "Clicking each real step opens the correct tool viewer; special ids do not crash.", "AS2", ""),
    ("AT2", "Unset-step gating", "R11-13", "AT",
     "Unset steps expose only the Scan tab with Scan Now disabled.",
     "For a step with no run, show only the Scan tab (Scan Now disabled, other option controls enabled); lock the other four tabs.",
     "Unset step -> Scan tab only, Scan Now disabled, options editable.", "AT1", ""),

    ("AU1", "Option change -> YAML update", "R11-14", "AU",
     "CliScanApp option changes update the editor YAML + diagram.",
     "Recompute the step's workflow YAML on option change and push via setYaml (or the editor's option-update message); viz updates.",
     "Change an option -> editor YAML + diagram reflect it.", "AT1, AS2", ""),
    ("AU2", "Validation -> enable Scan Now", "R11-15", "AU",
     "Scan Now enables only when the step's four sub-tasks validate.",
     "Enable Scan Now only on the editor's validationResult.ok for the step; drive the transition from editor messages.",
     "Invalid -> disabled; valid -> enabled; transition driven by validationResult.", "AU1", ""),

    ("AV1", "Scan Now -> execute -> four forms", "R11-16", "AV",
     "Scan Now runs the step and populates the four result tabs; scan_step persists.",
     "Call the SPEC-010 execute endpoint, show progress, populate Text/Structured/Graph/Report on completion; verify persistence by re-fetch. Needs SPEC-010 AN2.",
     "Live run on a lab/permissive target populates four tabs; re-fetch confirms persistence.", "AT1", ""),
    ("AV2", "Read-only replay", "R11-17", "AV",
     "A completed step loads its stored four forms read-only.",
     "Selecting an already-run step loads its persisted four forms read-only (all tabs viewable, Scan Now complete/disabled).",
     "Re-open a completed step -> four forms shown read-only.", "AV1", ""),

    ("AW1", "Import with temporary_id", "R11-18", "AW",
     "Exported scan graphs import as discrete subgraphs with fresh temporary_ids.",
     "`src/js/composer-temp-graph.js`: on a completed step with context.export scan_graph, assign each node temporary--<uuidv4>, remap edges, append as a discrete subgraph.",
     "Importing two graphs with overlapping canonical ids yields two independent subgraphs.", "AV1, AR3", ""),
    ("AW2", "Discrete render + remove toggle", "R11-19", "AW",
     "Accumulated imports render as discrete subgraphs with a per-subgraph remove.",
     "Render imports as discrete subgraphs on CanvasGraph; provide a remove toggle per imported subgraph.",
     "Multiple imports render discretely; remove drops one, leaving the rest.", "AW1", ""),
    ("AW3", "Strip-on-send round-trip", "R11-20", "AW",
     "Temporary graph sent to the server has temporary_ids stripped and edges remapped.",
     "On send, strip temporary_id and map edges back to nugget_instance_id (aligns with SPEC-010 R10-25).",
     "Captured outbound payload has no temporary_id; edges reference nugget_instance_id.", "AW1", ""),

    ("AX1", "Live E2E", "R11-21", "AX",
     "The full Composer flow works live against the v2 engine for a real target.",
     "Demonstrate: load project -> Composer -> select steps -> set options (YAML updates) -> run -> four forms -> exported graphs accumulate in the Temporary Subgraph Viewer -> temporary graph round-trips.",
     "Evidence attached; operator approval comment on THIS issue.",
     "AV2, AW3",
     "**OPERATOR SIGN-OFF.** Present the live E2E for operator sign-off; do not mark the SPEC-011 program done without an operator approval comment on THIS issue."),
    ("AX2", "GOV-08 exploratory review", "R11-22", "AX",
     "A GOV-08 scenario matrix over Projects + Composer is classified with tracked follow-ups.",
     "Run the scenario matrix (happy/empty/loading/error/cancel-collapse/invalid-options/keyboard/refresh) and classify each; file follow-ups for non-Validated.",
     "Review doc checked in with a completeness label; follow-up issues linked.", "AX1", ""),
]


def build_spec(repo: str, spec_tag: str, epics: dict, stories: list, spec_path_ref: str,
               foot: str, base_url: str) -> dict:
    codes: dict[str, dict] = {}
    print(f"\n=== {spec_tag} ({repo}) — epics ===")
    for code, (title, problem, spec_ids, children, success) in epics.items():
        info = gh_create(
            repo, f"[{spec_tag}] {title}",
            epic_body(spec_tag, problem, spec_ids, children, success, foot),
            ["epic", "enhancement", spec_tag.lower()],
        )
        codes[code] = info

    print(f"\n=== {spec_tag} ({repo}) — stories ===")
    for code, title, spec_ids, epic_code, outcome, scope, verify, blocked_by, gate in stories:
        parent = codes[epic_code]["number"]
        info = gh_create(
            repo, f"[{spec_tag}] {code} - {title}",
            child_body(spec_tag, code, parent, spec_ids, spec_path_ref, outcome, scope,
                       verify, blocked_by, gate, foot),
            ["story", "enhancement", spec_tag.lower()],
        )
        codes[code] = info
        if not DRY and parent and info["id"]:
            link_sub_issue(repo, parent, info["id"])
    return codes


def write_index_010(codes: dict) -> None:
    base = "https://github.com/brettforbes/spiderfeet/issues"

    def row(code: str, label: str, status: str) -> str:
        n = codes[code]["number"]
        return f"| {label} | [#{n}]({base}/{n}) | {status} |"

    lines = [
        "# SPEC-010 issue index (backend: spiderfeet)",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec010_011_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC010_AGENT_PLAN.md`",
        "**Spec:** `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`",
        "**Widget-side index:** `@spiderfeet-widget/.governance/project/SPEC011_WIDGET_ISSUE_INDEX.md`",
        "",
        "| Code | Issue | Status |",
        "|------|-------|--------|",
        row("AH", "Epic AH — IP disambiguation", "open"),
        row("AH0", "AH0 — Migration inventory", "open"),
        row("AH1", "AH1 — Catalogue split", "open"),
        row("AH2", "AH2 — Rules + code", "open"),
        row("AH3", "AH3 — Schema + docs + proj-07", "open"),
        row("AH4", "AH4 — Regenerate + re-verify", "open"),
        row("AI", "Epic AI — Schema reconcile + load", "open"),
        row("AI0", "AI0 — Edge-naming mapping doc", "open"),
        row("AI1", "AI1 — relates produced", "open"),
        row("AI2", "AI2 — fun JSON projections", "open"),
        row("AI3", "AI3 — Bootstrap load spiderfeet-actual", "open (G1 OPERATOR GATE)"),
        row("AJ", "Epic AJ — Port corpus → modules_v2/_core", "open"),
        row("AJ1", "AJ1 — Port _core engines", "open"),
        row("AJ2", "AJ2 — Port _rules + catalogues", "open"),
        row("AJ3", "AJ3 — typedb-driver client", "open"),
        row("AJ4", "AJ4 — Parity harness", "open"),
        row("AK", "Epic AK — Eight v2 CLI modules", "open"),
        row("AK0", "AK0 — _base + nmap rewrite", "open"),
        row("AK1", "AK1 — sfp_cli_netdiscover", "open"),
        row("AK2", "AK2 — sfp_cli_nerva", "open"),
        row("AK3", "AK3 — sfp_cli_pius", "open"),
        row("AK4", "AK4 — sfp_cli_subfinder", "open"),
        row("AK5", "AK5 — sfp_cli_httpx", "open"),
        row("AK6", "AK6 — sfp_cli_katana", "open"),
        row("AK7", "AK7 — sfp_cli_nuclei", "open"),
        row("AL", "Epic AL — TypeDB persistence", "open"),
        row("AL1", "AL1 — Entity CRUD", "open"),
        row("AL2", "AL2 — Dual-form subgraph serializer", "open"),
        row("AL3", "AL3 — JSON projection functions", "open"),
        row("AM", "Epic AM — Workflow DSL + GSE runtime", "open"),
        row("AM1", "AM1 — Parse/validate/schedule + GSE", "open"),
        row("AM2", "AM2 — YAML ↔ TypeDB conversion", "open"),
        row("AM3", "AM3 — Context export + merge", "open"),
        row("AN", "Epic AN — FastAPI v2 app", "open"),
        row("AN1", "AN1 — Absorb v1 + serve on 8001", "open (G2 OPERATOR GATE)"),
        row("AN2", "AN2 — New v2 routes", "open"),
        row("AN3", "AN3 — Route tests + v1 regression", "open"),
        row("AO", "Epic AO — Orchestrator", "open"),
        row("AO1", "AO1 — Single-step run", "open"),
        row("AO2", "AO2 — Full-workflow chaining", "open"),
        row("AP", "Epic AP — Backend acceptance", "open"),
        row("AP1", "AP1 — 4-target live run", "open (G3 OPERATOR GATE)"),
        row("AP2", "AP2 — Acceptance script", "open"),
        "",
        "## Execution order",
        "",
        "```",
        "AH0 -> AH1 -> AH2 -> AH3 -> AH4            (prerequisite for everything below)",
        "",
        "AI0 -> AI1 -> AI2 -> AI3 [G1: DB load]",
        "",
        "AJ1 -> AJ2 -> AJ3 -> AJ4",
        "  -> AK0 -> AK1..AK7                       (per-tool, parallelizable)",
        "",
        "AL1 -> AL2 -> AL3                          (after AI3 + AJ3)",
        "AM1 -> AM2 -> AM3                          (after AJ4; AM3 needs AL)",
        "",
        "AN1 [G2: 8001 cutover] -> AN2 -> AN3       (after AL + AM)",
        "AO1 -> AO2                                 (after AK + AL + AM)",
        "",
        "AP1 [G3: acceptance] -> AP2                (after AN + AO)",
        "```",
        "",
        "Lesser agents: pick next unblocked child; read the matching epic section in `SPEC010_AGENT_PLAN.md` first.",
        "Autonomous self-merge applies to every issue except the three operator gates G1 (AI3), G2 (AN1), G3 (AP1).",
        "",
    ]
    path = ROOT / ".governance" / "project" / "SPEC010_ISSUE_INDEX.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")


def write_index_011(codes: dict) -> None:
    base = "https://github.com/brettforbes/spiderfeet-widget/issues"

    def row(code: str, label: str, status: str) -> str:
        n = codes[code]["number"]
        return f"| {label} | [#{n}]({base}/{n}) | {status} |"

    lines = [
        "# SPEC-011 issue index (widget: spiderfeet-widget)",
        "",
        "Generated by `@spiderfeet/.seed/scripts/cli_corpus/create_spec010_011_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC011_AGENT_PLAN.md`",
        "**Spec:** `@spiderfeet/.governance/specs/SPEC-011-composer-projects-ui.md`",
        "**Backend index:** `@spiderfeet/.governance/project/SPEC010_ISSUE_INDEX.md`",
        "",
        "| Code | Issue | Status |",
        "|------|-------|--------|",
        row("AQ", "Epic AQ — API client + Projects page", "open"),
        row("AQ1", "AQ1 — v2 API client", "open"),
        row("AQ2", "AQ2 — Rename Enrichments→Projects + pane", "open"),
        row("AQ3", "AQ3 — Projects table", "open"),
        row("AQ4", "AQ4 — Project CRUD + row→Composer", "open"),
        row("AR", "Epic AR — Composer page shell", "open"),
        row("AR1", "AR1 — Composer pane + layout", "open"),
        row("AR2", "AR2 — Pane full-screen expand/revert", "open"),
        row("AR3", "AR3 — Two CanvasGraph viewers (empty Project Context)", "open"),
        row("AS", "Epic AS — Embed YAML editor iframe", "open"),
        row("AS1", "AS1 — Collapsing left iframe + width states", "open"),
        row("AS2", "AS2 — Handshake + load workflow YAML", "open"),
        row("AS3", "AS3 — Theme sync", "open"),
        row("AT", "Epic AT — Step selection → CliScanApp", "open"),
        row("AT1", "AT1 — stepSelected → right slide-in per tool", "open"),
        row("AT2", "AT2 — Unset-step gating", "open"),
        row("AU", "Epic AU — Option-edit round-trip + gating", "open"),
        row("AU1", "AU1 — Option change → YAML update", "open"),
        row("AU2", "AU2 — Validation → enable Scan Now", "open"),
        row("AV", "Epic AV — Live execute + replay", "open"),
        row("AV1", "AV1 — Scan Now → execute → four forms", "open (needs SPEC-010 AN2)"),
        row("AV2", "AV2 — Read-only replay", "open"),
        row("AW", "Epic AW — Temporary Subgraph Viewer", "open"),
        row("AW1", "AW1 — Import with temporary_id", "open"),
        row("AW2", "AW2 — Discrete render + remove toggle", "open"),
        row("AW3", "AW3 — Strip-on-send round-trip", "open"),
        row("AX", "Epic AX — Widget acceptance", "open"),
        row("AX1", "AX1 — Live E2E", "open (OPERATOR SIGN-OFF)"),
        row("AX2", "AX2 — GOV-08 exploratory review", "open"),
        "",
        "## Execution order",
        "",
        "```",
        "AQ1 -> AQ2 -> AQ3 -> AQ4",
        "AR1 -> AR2 -> AR3                 (after AQ2)",
        "AS1 -> AS2 -> AS3                 (after AR1)",
        "AT1 -> AT2                        (after AS2)",
        "AU1 -> AU2                        (after AT + AS)",
        "AV1 -> AV2                        (after AT; needs SPEC-010 AN2 execute API)",
        "AW1 -> AW2 -> AW3                 (after AV1)",
        "AX1 [OPERATOR SIGN-OFF] -> AX2    (after AV + AW)",
        "```",
        "",
        "Lesser agents: pick next unblocked child; read the matching epic section in `SPEC011_AGENT_PLAN.md` first.",
        "AQ–AU can proceed against the documented SPEC-010 contract with a local stub; AV/AW need the live SPEC-010 AN2 endpoints.",
        "Autonomous self-merge applies to every issue except the AX1 operator sign-off gate.",
        "",
    ]
    path = WIDGET_ROOT / ".governance" / "project" / "SPEC011_WIDGET_ISSUE_INDEX.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")


def main() -> None:
    global DRY
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--spec", choices=["010", "011", "both"], default="both")
    args = ap.parse_args()
    DRY = args.dry_run

    if args.spec in ("010", "both"):
        if not DRY:
            ensure_label(REPO_BACKEND, "story", "0E8A16", "Child story under a SPEC epic")
            ensure_label(REPO_BACKEND, "spec-010", "1D76DB", "SpiderFeet v2 engine (SPEC-010)")
        codes = build_spec(REPO_BACKEND, "SPEC-010", EPICS_010, STORIES_010,
                           SPEC010_SPECPATH, FOOTER_010,
                           "https://github.com/brettforbes/spiderfeet/issues")
        if not DRY:
            write_index_010(codes)

    if args.spec in ("011", "both"):
        if not DRY:
            ensure_label(REPO_WIDGET, "story", "0E8A16", "Child story under a SPEC epic")
            ensure_label(REPO_WIDGET, "spec-011", "1D76DB", "Composer/Projects widget UI (SPEC-011)")
        codes = build_spec(REPO_WIDGET, "SPEC-011", EPICS_011, STORIES_011,
                           SPEC011_SPECPATH, FOOTER_011,
                           "https://github.com/brettforbes/spiderfeet-widget/issues")
        if not DRY:
            write_index_011(codes)

    print("\nDone." if not DRY else "\nDry run complete — no issues created.")


if __name__ == "__main__":
    main()
