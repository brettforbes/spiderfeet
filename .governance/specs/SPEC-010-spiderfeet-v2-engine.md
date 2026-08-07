# SPEC-010 — SpiderFeet v2 engine: modules_v2, FastAPI, TypeDB `spiderfeet-actual`

**Status:** Active
**Parent coordination:** Source prompt `.seed/17_SpiderFeet_v2_Integrating_TypeDB_FastAPI_iFrame.md`; follow-on to SPEC-004/005/006/007/008
**Plan / agent playbook:** `.governance/project/SPEC010_AGENT_PLAN.md`
**Issue index (this repo):** `.governance/project/SPEC010_ISSUE_INDEX.md`
**Companion spec (widget UI):** `.governance/specs/SPEC-011-composer-projects-ui.md`
**Skills:** `.cursor/skills/typedb/SKILL.md`, `.cursor/skills/typedb-bridge/SKILL.md` (type-bridge remains deferred — see R10-13)

## Objective

Build the **v2 SpiderFeet engine**: a FastAPI service backed by TypeDB (`spiderfeet-actual`, loaded from `.seed/spiderfeet_v2_semantic.tql`) that runs YAML-DSL workflows over the 8 CLI-app modules, produces the **four output forms** (Text · Structured · Semantic Graph · Narrative Report) per scan step from a common ontology, stores each scan step and its subgraph, and combines scan subgraphs into project and temporary contexts.

The engine is assembled by **porting the production CLI-corpus machinery** (`.seed/scripts/cli_corpus/core` + `adapters` + `rules`) into a **self-contained `modules_v2/`** tree, then implementing real four-output modules (`modules_v2/sfp_cli_<tool>.py`) for all 8 tools, and standing up the workflow runtime, persistence, and API in a new `spiderfeet_v2/` package.

A prerequisite correction runs first: the ambiguous **`IP_ADDRESS`** nugget is split into **`IPV4_ADDRESS`** and **`IPV6_ADDRESS`** across the canonical CLI-profiling stack, driven by the centralized address-parsing code (`core/ip_classify.py`).

## Non-goals

- Widget UI (Projects page, Composer page, iframe wiring, live-execute UI) — that is **SPEC-011**.
- Rewriting production v1 `sfp_*` OSINT modules or the `sfp-api-*` service catalogue.
- Onboarding CLI tools beyond the 8 already formally examined (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei).
- The Project Context Viewer combine/merge **rule system** (adding subgraphs into the final project context) beyond the append-unique v1 merge — deeper context reconciliation is a future spec.
- Migrating to `typedb-bridge` generated models — stays deferred (issue #42); v2 uses `typedb-driver` directly (R10-13).
- Deleting the original `.seed/scripts/cli_corpus/` tree — it stays as-is; deletion is a separate later cleanup (operator decision).

## Requirements

### Epic AH — IP_ADDRESS → IPV4_ADDRESS / IPV6_ADDRESS disambiguation (prerequisite)

| ID | Requirement |
|----|-------------|
| R10-01 | `core/ip_classify.py` is the single source of truth for classifying an address literal into `IPV4_ADDRESS` or `IPV6_ADDRESS`; the ambiguous `IP_ADDRESS` nugget id is removed from all v2/corpus code paths. A written inventory (`.governance/project/SPEC010_IP_MIGRATION_INVENTORY.md`) enumerates every occurrence across code, rules, catalogues, schema, docs, and generated artifacts. |
| R10-02 | `nuggets.json` / `nuggets_extension.json` catalogues define `IPV4_ADDRESS` and `IPV6_ADDRESS` (id, type ENTITY, description, colour, icon); `AFFILIATE_IPADDR`/`BLACKLISTED_IPADDR`/`MALICIOUS_IPADDR` and any other `IP_ADDRESS`-derived variants are audited and split or retained per the inventory. New/changed types go in `nuggets_extension.json` only. |
| R10-03 | All 8 tool rule packs (`.seed/scripts/cli_corpus/rules/<tool>/*.yaml`) and adapter/topology/correlation code that emit or match `IP_ADDRESS` are updated to produce/consume `IPV4_ADDRESS`/`IPV6_ADDRESS` via `classify_ip`. No literal `IP_ADDRESS` remains in emitting code. |
| R10-04 | The v2 TypeDB schema (`.seed/spiderfeet_v2_semantic.tql`) uses `ipv4-address` / `ipv6-address` entities consistently; any `ip-address` remnant is reconciled. Structure docs (`.docs/docs-for-cli-tools/nugget_structure/*.md`, `_Current_Ontology.md`) reflect the split. |
| R10-05 | All affected generated example artifacts (proposed graph JSON + narrative MD under `.docs/docs-for-cli-tools/`, and widget content bundles `modules_v2/content/<tool>/graph_structure.md`) are regenerated via the backfill scripts and re-verified: no `IP_ADDRESS` node, no orphan nodes, IPv4/IPv6 nodes carry the correct id. A repo-wide grep proves `IP_ADDRESS` survives only in intentional legacy/historic locations recorded in the inventory. |

### Epic AI — v2 semantic schema reconciliation + `spiderfeet-actual` load

| ID | Requirement |
|----|-------------|
| R10-06 | Semantic-edge naming is reconciled end-to-end: the graph JSON relation names (`had` / `contains` / `listens-to`) and the TypeQL relation types (`has_this` / `contains_this` / `listens_to_this`) have one documented canonical mapping, applied consistently in the load/serialize layer. The seed §3.2 example (`container`/`contained`, `contains`) is reconciled to the schema's `source`/`target` on `*_this`. |
| R10-07 | `scan_step` gains `relates produced @card(0..)` (the schema currently declares `nugget plays scan_step:produced` with no matching `relates produced`); the produced-nuggets role round-trips. |
| R10-08 | TypeQL `fun` queries return JSON-serializable projections for: a project (with its workflows, targets, project_context, temporary_subgraph), a workflow (first/prior/next steps + target), a scan_step (its four UI forms + consumed/produced nuggets + scan_result_graph), and `contains_recursive` extended to also return `had` and `listens-to` edges within a meta-concept subgraph. |
| R10-09 | `spiderfeet_v2/db/bootstrap` loads `.seed/spiderfeet_v2_semantic.tql` into a fresh `spiderfeet-actual` database and seeds the 8 `sfp-cli-app-*` osint-service records; `--reset` recreates cleanly and idempotently. **[OPERATOR GATE G1 — see plan §0.1]** |

### Epic AJ — Port CLI-corpus engine into self-contained `modules_v2/_core`

| ID | Requirement |
|----|-------------|
| R10-10 | `modules_v2/_core/` contains a self-contained copy of the corpus engine (`rule_engine`, `narrative_engine`, `graph_builder`, `topology`, `ip_classify`, `structure_doc_engine`, `correlation_engine`, `correlation_lists`, `narrative_profile`, `types`, `narrative_report`) with imports rewritten to `modules_v2._core.*` — no import from `.seed/scripts/cli_corpus`. |
| R10-11 | `modules_v2/_rules/` contains the ported YAML rule packs (`_shared/` + per-tool `mapping.yaml`/`narrative.yaml`/`structure.yaml`) and `modules_v2/_core` resolves them from within `modules_v2/`. Catalogues (`nuggets.json` + `nuggets_extension.json`) are loadable by the ported `graph_builder` from a location under `modules_v2/` (copied or referenced via a single configurable path). |
| R10-12 | Parity test: for each of the 8 tools, running the ported `_core` pipeline over a recorded structured fixture produces graph + narrative output byte-equivalent (or explainably equivalent) to the original `cli_corpus` output for the same fixture, incorporating the AH IPv4/IPv6 split. |
| R10-13 | `spiderfeet_v2/db/` TypeDB client uses `typedb-driver` directly (mirroring `spiderfeet/map/connection.py` + `config.py`), targeting `spiderfeet-actual`; no `typedb-bridge` dependency is added. |

### Epic AK — Eight v2 CLI modules (four-output)

| ID | Requirement |
|----|-------------|
| R10-14 | `modules_v2/_base.py` defines the v2 module contract: `run(scan_step_spec) -> {command, text, structured, structured_type, graph, narrative, status, counts, duration, timestamp}`, using `_core`. The nmap stub (`modules_v2/sfp_cli_nmap.py`) is rewritten to real, importable, four-output code and its current syntax errors are fixed. |
| R10-15 | `modules_v2/sfp_cli_<tool>.py` exists and is import-clean for all 8 tools (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei); each declares `module_id`, consumed inputs, produced nugget types, option/argv schema, and produces the four forms from a live CLI run via `_core`. |
| R10-16 | Each module runs a real live scan (env has TypeDB + all 8 CLI tools in WSL) and produces all four forms with the structured-first law honoured (structured mode used whenever the tool offers one; text derived from structured). Per-tool smoke evidence is captured. |

### Epic AL — TypeDB persistence layer + JSON projections

| ID | Requirement |
|----|-------------|
| R10-17 | `spiderfeet_v2/db/` implements CRUD for `project`, `workflow`, `target`, `scan_step`, and the three subgraph subtypes (`scan_result_graph`, `project_context`, `temporary_subgraph`), each round-tripping to/from a JSON object shape usable by the API and widget. |
| R10-18 | Subgraphs persist in **both** forms per seed §3.3: the `json-string` attribute form and the in-graph entity/relation form (nuggets + edges), with a documented single serializer/deserializer bridging graph JSON ↔ TypeDB. |
| R10-19 | The `fun`-driven read queries from R10-08 are exposed as Python functions returning JSON; a scan_step round-trips its four UI forms and consumed/produced nuggets losslessly. |

### Epic AM — Workflow DSL + GSE runtime

| ID | Requirement |
|----|-------------|
| R10-20 | The SPEC-007 workflow DSL + GSE evaluation (`.seed/scripts/cli_workflow/` + schemas `workflow_v1.schema.json`, `gse_v1.schema.json`) is integrated into `spiderfeet_v2/`: parse+validate a workflow YAML, schedule its step DAG (`needs`), resolve `input.from`, build argv/files, and evaluate `output.vars` GSE bindings against a step's scan graph. Canonical authoring shape is 12A (`apiVersion: spiderfeet.workflow/v1`, list `steps`). |
| R10-21 | Bidirectional conversion between a workflow's TypeDB representation (`workflow`/`scan_step`/`target` entities+relations, incl. `workflow_yaml`/`scan_yaml`/`target_yaml` string attributes) and the YAML-DSL/JSON form, so a workflow created/edited in either place stays consistent. |
| R10-22 | A step's `context.export: scan_graph` marks its scan_result_graph for export to the temporary context; `none` does not. The temporary-context merge is append-unique (unique nodes by id, unique edges by `(source,target,relation)`) per 12B v1. |

### Epic AN — FastAPI v2 app (absorb v1 routers + new v2 routes)

| ID | Requirement |
|----|-------------|
| R10-23 | `spiderfeet_v2/api/` FastAPI app becomes **the** app served on `127.0.0.1:8001/api/v1`, **absorbing the existing v1 routers** the widget already consumes (map, tests, subscriptions, cli-corpus, content) so nothing currently working in the widget breaks. CORS + stable base URL retained. **[OPERATOR GATE G2 — 8001 cutover, see plan §0.1]** |
| R10-24 | New v2 routes: projects CRUD, workflows CRUD, targets CRUD, workflow execution (run a step / run a workflow), scan_step retrieval (four forms), and temporary/project context read + temporary-context update (with temporary-id stripping per R10-25). Pydantic models; OpenAPI examples for the core routes. |
| R10-25 | The temporary-context update endpoint accepts the widget's temporary-id-tagged nodes/edges, strips `temporary_id`, and maps edges back to canonical `nugget_instance_id` before persisting (server never stores `temporary_id`). |
| R10-26 | pytest coverage for the new v2 routes; a regression check confirms the absorbed v1 routes still return equivalent responses (Maps/Tests/Subscriptions/CLI-Profiling unaffected). |

### Epic AO — Workflow orchestrator

| ID | Requirement |
|----|-------------|
| R10-27 | The orchestrator runs a workflow step: resolve inputs → invoke the module (AK) → capture the four forms → persist a `scan_step` + `scan_result_graph` (AL) → evaluate `output.vars` (AM) → export to temporary context when `context.export: scan_graph`. Step status lifecycle (`STARTING`…`SUCCESS`/`ERROR`) is recorded. |
| R10-28 | Running a full workflow chains steps by `needs`, threading output vars from prior steps into later steps' `input.from`, and accumulates exported scan graphs into the project's temporary context. |

### Epic AP — Backend end-to-end acceptance (4 targets)

| ID | Requirement |
|----|-------------|
| R10-29 | The 12A split-branch workflow runs end-to-end against each of the 4 example targets (sbs.com.au, k2am.com.au, venturecapitalopportunitiesfund.com.au, squarepeg.vc) via live scans; each step yields four forms, a persisted scan_step + subgraph, and (where `export: scan_graph`) a temporary-context contribution. Evidence bundle recorded. **[OPERATOR GATE G3 — final acceptance sign-off, see plan §0.1]** |
| R10-30 | An acceptance script (`spiderfeet_v2/acceptance/run_four_targets.py` or equivalent) reproduces the run and validates: no `IP_ADDRESS` nodes, no orphan nodes, correct four-form storage, and queryable project/workflow/step/context JSON via the API. |

## Milestone (what "done" looks like for the operator)

Loading TypeDB `spiderfeet-actual`, starting the v2 FastAPI on 8001 (with Maps/Tests/Subscriptions/CLI-Profiling still working), then running the 12A workflow against any of the 4 real targets: every step stores and returns its Text / Structured / Semantic-Graph / Narrative forms, scan subgraphs land in the temporary context, and the whole project/workflow/step/context structure is retrievable as JSON through the API — with every address node unambiguously `IPV4_ADDRESS` or `IPV6_ADDRESS`. SPEC-011 consumes exactly this API.

## Architecture

```text
modules_v2/
  _core/            ← ported cli_corpus/core (rule_engine, narrative_engine, graph_builder,
                       topology, ip_classify, structure_doc_engine, correlation*, narrative_report)
  _rules/           ← ported rule packs (_shared/ + per-tool yaml) + nugget catalogues
  _base.py          ← v2 module contract (four-output run())
  sfp_cli_nmap.py … sfp_cli_nuclei.py   ← 8 real four-output modules
  content/<tool>/   ← SPEC-008 content bundles (graph_structure.md regenerated by AH)

spiderfeet_v2/
  db/               ← typedb-driver client, config, bootstrap (spiderfeet-actual), CRUD, fun projections
  workflow/         ← DSL parse/validate/schedule + GSE eval + YAML↔TypeDB conversion
  engine/           ← orchestrator (step → module → 4 forms → persist → export)
  api/              ← FastAPI app on 8001: absorbed v1 routers + new v2 routes
  acceptance/       ← 4-target end-to-end script + evidence

.seed/spiderfeet_v2_semantic.tql   ← reconciled schema, loaded into spiderfeet-actual
```

## Traceability

Implementation: GitHub epics under `[SPEC-010]` in `brettforbes/spiderfeet`. Epic letters `AH`–`AP` (continuing after SPEC-009's `AB`–`AG`). Widget consumption is `[SPEC-011]` (epics `AQ`–`AX`, widget repo). Requirement IDs `R10-01`…`R10-30`.
