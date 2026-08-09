# SPEC-013 — Projects & Composer refinement (phase 2)

**Status:** Draft (awaiting operator approval to open issues)
**Source prompt:** `.seed/18_Refining_the_Projects_and_Composer.md`
**Parents (extends, does not replace):**
- Backend engine — `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
- Composer/Projects widget UI — `.governance/specs/SPEC-011-composer-projects-ui.md`
- YAML DSL Workflow iFrame — `@yaml-workflow-widget/.governance/specs/SPEC-012-update-widget.md` + `SPEC-012-LAYOUT-RULES.md`

**Repos in scope (split delivery):**
| Repo | Role in this phase |
|------|--------------------|
| `spiderfeet` | Project schema/CRUD/API alignment; YAML↔TypeDB round-trip; 5 seed projects |
| `spiderfeet-widget` | UI density; navbar auto-hide; Projects page refinement; Composer project dropdown + Workflow Bar controls |
| `yaml-workflow-widget` | Remove DAG title bar; host-driven edit/settings; embed layout fix; zoom/pan rework; fit rules; legend toggle |

**Issue indexes:**
- Backend — `.governance/project/SPEC013_ISSUE_INDEX.md`
- Widget — `@spiderfeet-widget/.governance/project/SPEC013_WIDGET_ISSUE_INDEX.md`
- YAML widget — `@yaml-workflow-widget/.governance/project/SPEC013_ISSUE_INDEX.md`

---

## 0. Operator-confirmed decisions (grill outcomes)

These were confirmed with the operator before drafting and are binding for all executors:

1. **YAML lives on the workflow, never a local file.** `workflow.workflow_yaml` is the string form; the parsed structure (target + scan_steps + DAG edges) is also materialized in TypeDB. The project carries `project_name`, `project_description`, `project_created` (+ optional `stix_incident_id`). No `project_yaml` attribute is introduced.
   - **Schema shape (operator-revised 2026-08-09):** `project` is now an **entity** (`plays workflow:project`, `plays project_context:project`, `plays temporary_subgraph:project`); `workflow` is a **relation** that `relates project @card(0..1)` (plus `first_step`/`prior_step`/`next_step`/`target`). The old `project`-as-relation shape is gone. Executors must flip every place that assumed the old direction (see §0.1 and R13-01/02).
2. **Latest emitted YAML wins.** The YAML DSL Workflow iFrame validates with its Langium grammar, so whatever it emits is authoritative. Every emitted YAML must be disassembled by the backend and stored **both** as the `workflow_yaml` string **and** as live TypeDB schema objects (workflow, target, scan_steps, edges). This applies on create, on seed, and on every edit round-trip.
3. **New project** = create the project + a workflow whose YAML is **info-only** (`apiVersion`, `kind`, `id`, filled `info{name,description,author,created}`; no `inputs`/`target`/`steps`). Persist to TypeDB via FastAPI so `GET /projects` immediately returns the new row; then redirect to the Composer with that workflow loaded.
4. **5 seed projects**, fully materialized in TypeDB with no scan results yet:

   | # | Input | Template | Project name | Description |
   |---|-------|----------|--------------|-------------|
   | 1 | none | `12A2_Workflow_YAML_Example.yaml` | Simple Wireless Scan | Simple local-network wireless/ARP discovery scan |
   | 2 | www.sbs.com.au | `12A_Workflow_YAML_Example.yaml` | Attack Surface Recon — www.sbs.com.au | Twin-fork attack-surface recon of www.sbs.com.au |
   | 3 | www.k2am.com.au | `12A_Workflow_YAML_Example.yaml` | Attack Surface Recon — www.k2am.com.au | Twin-fork attack-surface recon of www.k2am.com.au |
   | 4 | www.venturecapitalopportunitiesfund.com.au | `12A_Workflow_YAML_Example.yaml` | Attack Surface Recon — www.venturecapitalopportunitiesfund.com.au | Twin-fork attack-surface recon of that domain |
   | 5 | www.squarepeg.vc | `12A_Workflow_YAML_Example.yaml` | Attack Surface Recon — www.squarepeg.vc | Twin-fork attack-surface recon of www.squarepeg.vc |

   Clones 2–5 each get a **fresh** `project_id` and `workflow_id` (uuidv4) and a rewritten `inputs.targets.values` = `[https://<input>]`. Names/descriptions are distinct (target appended).
5. **"NetworkError" fix = resilience.** The widget dev server is on `:4001` (already CORS-allowed), so the cause is the API being unreachable. Make the Projects page show a friendly "backend unreachable" state with retry, verify base URL + CORS, and document how to start the API. No fake data.
6. **Navbar auto-hide** on every tab: slide up after ~3s idle (and after navigating); reveal when the cursor is within ~48px of the top edge or on keyboard focus.
7. **Composer Workflow Bar controls** = only a **pencil** icon (toggles to **spectacles** when editing) and a **gear** icon. Gear opens the iFrame settings and additionally can **hide the legend**. The old title-bar functions (YAML dump, layout dump) are dropped.
8. **Persistence save points:** the widget persists the current editor YAML (PUT re-parse) when the user leaves edit mode (clicks spectacles) **and** when they click **Run Workflow**.
9. **Backend round-trip:** `PUT /workflows/{id}` accepts the new `workflow_yaml`, re-parses it, and transactionally replaces that workflow's steps/target/edges. `GET /projects/{id}/complete` returns the project + its workflow(s) with `workflow_yaml` inline for a one-call Composer load.
10. **YAML widget zoom/pan:** `CTRL +` / `CTRL -` keys **and** `CTRL`+mouse-wheel zoom; plain mouse-wheel = vertical pan (right-edge scrollbar); click-drag = pan both axes. Reset-to-default view is an **on-canvas** control.
11. **Density** is its own first widget epic. **Spec placement** is split (this master + mirrored issue indexes). **Execution** is sequential, one issue at a time, governance = branch → PR → close issue with a completion note → merge before continuing; verification = build/lint/targeted tests + a manual UI-check note, with full live end-to-end deferred to a per-repo acceptance issue.

### 0.1 Schema-direction change + playerless note (executors MUST read)

The operator revised the schema so **`project` is an entity and `workflow` is the relation** (`workflow relates project @card(0..1)`; `project plays workflow:project`). This resolves the earlier playerless concern:

- A **new, empty project** is just an `project` **entity** — it needs no role players and persists on its own.
- An **info-only workflow** relation is valid because it links to its project (`links (project: $proj)`) — that single player satisfies TypeDB 3. **No placeholder `target` is needed.**

**Ripple to fix (this is real work, tracked in R13-01/R13-02):** the current Python + schema functions still assume `project` was a relation and are now wrong:
- `crud.py::create_project` inserts `$p isa project ... links (workflow: $w)` — rewrite: insert `project` as an entity; link workflows by giving each `workflow` relation `links (project: $p)`.
- `crud.py::get_project`/`list_projects`/`update_project` — query workflows via `$w isa workflow, links (project: $p)` (inverted direction).
- `workflow/typedb_convert.py` workflow forms — add the optional `project` link; keep `first_step`/`prior_step`/`next_step`/`target`.
- `db/projections.py::get_project` and the `project_workflow_ids` schema function (`.tql`) — flip to the workflow-relates-project direction.
- `api/schemas.py` `ProjectCreate` no longer needs `workflow_ids` (an entity project is valid standalone); the new-project service (R13-04) creates the info-only workflow and links it to the project.

---

## 1. Objective

Refine the already-delivered Projects and Composer pages (SPEC-011) and the embedded YAML DSL Workflow iFrame (SPEC-012) so that:

- Projects are real, first-class records (name/description/created) seeded with 5 runnable-but-unrun examples;
- creating, opening, and editing a project reliably round-trips YAML ⇄ TypeDB;
- the Composer chrome is denser, the navbar auto-hides, projects are selectable from a Composer dropdown, and the workflow editor is driven by a minimal pencil/gear control set;
- the DAG viz displays correctly at partial width (no embed overlays), with predictable zoom/pan/fit behavior.

## 2. Non-goals

- The workflow **execution/run** engine and four-forms population — already SPEC-010/011 (AV/AW). This phase only persists YAML and materializes structure; it does not change how scans run.
- Rebuilding `CliScanApp`, `CanvasGraph`, or the WorkflowSeed layout goldens (SPEC-012 L0) — reused as-is.
- Populating the Project Context Viewer (remains empty per SPEC-011).
- New OSINT modules or nugget-ontology changes.

---

## 3. Requirements

### Backend (`spiderfeet`)

#### Epic B1 — Project schema, CRUD & API alignment

| ID | Requirement |
|----|-------------|
| R13-01 | `.seed/spiderfeet_v2_semantic.tql`: declare the attribute types `project_name`, `project_description`, `project_created`; finalize `project` as an **entity** (`project_id @key`, `stix_incident_id @card(0..1)`, name/description/created; `plays workflow:project`, `plays project_context:project`, `plays temporary_subgraph:project`) and `workflow` as a **relation** with `relates project @card(0..1)`. Update the `project_workflow_ids` (and any related) schema **functions** to the workflow-relates-project direction. Schema loads cleanly on `spiderfeet-actual` (typedb-check / schema tx); data-safe reload documented. Follow the typedb skill load checklist. |
| R13-02 | Flip the Python layer to the new direction (§0.1): `crud.py` (`PROJECT_ATTRS` + create/get/update/list_project — project as entity, workflows linked via `workflow links (project: $p)`), `workflow/typedb_convert.py` (workflow forms carry optional `project` link), `db/projections.py::get_project`. Handle `project_name`/`project_description`/`project_created`; no attribute/direction drift vs schema. |
| R13-03 | `api/schemas.py` `ProjectCreate` / `ProjectUpdate` / `ProjectOut` expose `project_name`, `project_description`, `project_created`, optional `stix_incident_id`; `ProjectCreate` no longer requires `workflow_ids` (an entity project is valid standalone). OpenAPI reflects the new shape. |

#### Epic B2 — YAML ⇄ TypeDB round-trip & project lifecycle API

| ID | Requirement |
|----|-------------|
| R13-04 | Info-only workflow generator + create-new-project service: given name/description (author default, created=now, generated `project_id`/`workflow_id`), create the `project` entity, emit the info-only YAML, and create the `workflow` relation linked to the project (`links (project: $p)`) with `workflow_yaml` = info-only. No target/steps and **no placeholder target** (§0.1). Exposed via `POST /projects` (or a dedicated create route) so the new row appears in `GET /projects`. |
| R13-05 | `PUT /workflows/{workflow_id}` accepts a new `workflow_yaml`, re-runs the YAML→TypeDB converter (`persist_workflow_yaml`, replace=True) transactionally so steps/target/edges + `workflow_yaml` all reflect the latest emitted YAML. Returns the updated workflow projection. Invalid YAML is rejected without corrupting the stored bundle. |
| R13-06 | `GET /projects/{project_id}/complete` returns the project attributes + each linked workflow with `workflow_yaml` inline (and a parsed step/target summary), so the Composer loads a project in one call. |

#### Epic B3 — Seed 5 projects + verification

| ID | Requirement |
|----|-------------|
| R13-07 | An idempotent seed script (under `.seed/scripts/`) creates the 5 projects of §0.4 in `spiderfeet-actual`: project 1 from `12A2`, projects 2–5 as `12A` clones with fresh ids and rewritten `inputs.targets.values`, distinct names/descriptions. Each workflow is fully materialized (target + every scan_step + DAG edges via `persist_workflow_yaml`) with **no scan results** (`scan_step` UI/result fields empty). |
| R13-08 | Verification step queries `spiderfeet-actual` and asserts: 5 projects present; project 1 has 1 step (netdiscover) and no target-input; each clone has the 6 subfinder→nmap/nerva + httpx/katana/nuclei steps and the expected DAG edges; no `scan_result_graph`/results exist. Result recorded in the issue. |
| R13-09 | pytest coverage for R13-02/03/04/05/06 (project attrs round-trip, PUT re-parse replace semantics, `/complete` shape) plus the seed verification, runnable via `poetry run pytest`. |

### Widget (`spiderfeet-widget`)

#### Epic W1 — UI density pass

| ID | Requirement |
|----|-------------|
| R13-10 | Reduce global vertical chrome so content sits close to the screen edges: navbar logo height, per-pane toolbar `py`, and content wrapper padding across all panes (Projects, Composer, Maps, Tests, Subscriptions, CLI Profiling, Settings). No functional/layout regressions; verified visually on each pane. |

#### Epic W2 — Navbar auto-hide

| ID | Requirement |
|----|-------------|
| R13-11 | The top navbar slides up out of view after ~3s idle and after a tab navigation, enlarging every page. It slides back down when the cursor comes within ~48px of the top edge or on keyboard focus/tab-key. Smooth transition; accessible (focusable reveal, respects reduced-motion). State does not trap the user on any pane. |

#### Epic W3 — Projects page refinement

| ID | Requirement |
|----|-------------|
| R13-12 | The Projects table columns match the `project` schema: **Name**, **Description**, **Created**, **Workflows** (count), optional **STIX incident id**, plus existing row actions. Rendered from `GET /projects`. |
| R13-13 | Resilient load: on fetch failure show a friendly "Backend unreachable — is the API running on :8001?" state with a Retry control and auto-retry; distinguish empty (no projects) from error; no raw stacktrace / red NetworkError dump. |
| R13-14 | New Project modal collects **Name** + **Description** (editable), and shows read-only generated **Project ID** (`project--<uuidv4>`) and **Created** (now). Create calls the backend create flow (R13-04) and, on success, redirects to the Composer with the new project loaded. |
| R13-15 | **Double-click** a project row opens it in the Composer (loads via `GET /projects/{id}/complete` → `setYaml` into the iFrame). Single-click selects/highlights the row. |

#### Epic W4 — Composer project dropdown + Workflow Bar controls

| ID | Requirement |
|----|-------------|
| R13-16 | The Composer top bar gains a **project dropdown** (near the "Composer / <project>" label). Its top item is an **"Add new project"** checkbox that, when checked, opens the New Project modal (R13-14); otherwise the dropdown lists existing projects. Selecting a project loads it (via `/complete`) into the iFrame and updates the label. |
| R13-17 | The Workflow Bar gains a **pencil** icon (→ **spectacles** when editing) that toggles the iFrame edit/read-only mode, and a **gear** icon that opens the iFrame settings. Buttons drive the iFrame via the new postMessages (R13-21). No YAML/layout-dump buttons. |
| R13-18 | The widget persists the current editor YAML via `PUT /workflows/{id}` (R13-05) **when the user leaves edit mode** (clicks spectacles) **and when Run Workflow is clicked**. Persistence is verified by re-fetch (source-of-truth proof, not toast-only). |

#### Epic W5 — Widget acceptance

| ID | Requirement |
|----|-------------|
| R13-19 | GOV-08 exploratory review of the refined Projects + Composer pages against the live backend + seeded projects: scenario matrix (happy, empty, loading, error/unreachable, create, double-click open, dropdown select + add-new, edit→persist round-trip, navbar hide/reveal, density) classified with tracked follow-ups. **[OPERATOR GATE]** |

### YAML widget (`yaml-workflow-widget`)

#### Epic Y1 — Remove title bar + host-driven controls

| ID | Requirement |
|----|-------------|
| R13-20 | The "CLI Workflow DAG" title bar (`App.vue` L7–81) is removed in **all** modes (embed and standalone). Edit-mode and settings are still reachable — via host postMessages when embedded, and via minimal on-canvas affordances when standalone. |
| R13-21 | New host→iframe messages added and documented in `HOST_PROTOCOL.md`: `setEditMode {editing}` (with `editModeChanged` echo), `openSettings`, `setLegendVisible {visible}`. Existing `setYaml`/`getYaml`/`setTheme`/`selectStep` and outbound `yamlChanged`/`validationResult`/`stepSelected`/`themeChanged` are preserved. |

#### Epic Y2 — Embed layout fix

| ID | Requirement |
|----|-------------|
| R13-22 | Remove the embed viewport-reduction (`.dag-host.embed .embed-diagram { max-width:33.333%; margin:0 auto }` and any related overlays/side bands). In embed/partial-width the diagram renders full-bleed and centered: no left/right empty thirds, the vertical scrollbar sits at the far right edge, and the legend anchors correctly (not over the diagram). Reproduce-and-fix the 5 symptoms listed in `.seed/18` §2.2.5. |

#### Epic Y3 — Dimensions + fit rules

| ID | Requirement |
|----|-------------|
| R13-23 | Track the DAG bounding geometry at 100% zoom: vertical centre line, full width left-of-centre and right-of-centre, and top/bottom, updated on every layout change. |
| R13-24 | Default view = **70%** zoom, DAG centered horizontally, **Start** shape at the top, remainder reachable by vertical scroll. If the DAG is wider than the host at that zoom, zoom out until the left/right edges are **10px** inside the host edges (graph width + 10px each side). Host Workflow Bar **reset** control restores this default (or fullscreen split when left column is full). |

#### Epic Y4 — Zoom/pan rework + legend toggle

| ID | Requirement |
|----|-------------|
| R13-25 | Zoom via `CTRL +` / `CTRL -` keys **and** `CTRL`+mouse-wheel. Plain mouse-wheel pans vertically (far-right scrollbar). Click-drag pans both axes. Existing zoom clamps preserved/adjusted to support the fit rules. |
| R13-26 | The settings panel gains a **Show legend** toggle (default on) that shows/hides `EdgeLegend`, also driven by the host `setLegendVisible` message. Existing theme + coloured-edges options preserved. |

#### Epic Y5 — YAML widget acceptance

| ID | Requirement |
|----|-------------|
| R13-27 | Smoke + visual verification on both seed workflows (`12A`, `12A2`) in embed and standalone: title bar gone; embed renders full-bleed with correct scrollbar/legend; default **70%**/fit view correct; CTRL zoom + wheel/drag pan behave per R13-25; pencil/gear/reset host messages toggle edit + settings + legend + view reset. Screenshots attached. **[OPERATOR GATE]** |

---

## 4. Execution order & cross-repo dependencies

```
Backend:   B1(R13-01→02→03) → B2(R13-04, R13-05, R13-06) → B3(R13-07→08→09)
Widget:    W1(R13-10) ∥ W2(R13-11)            [independent, do early]
           W3(R13-12→13→14→15)                [needs B1..B3 + R13-06]
           W4(R13-16→17→18)                   [needs W3 + Y1(R13-21) + B2(R13-05)]
           W5(R13-19)                          [OPERATOR GATE, after W3+W4+backend+yaml]
YAML:      Y1(R13-20→21) → Y2(R13-22) → Y3(R13-23→24) → Y4(R13-25→26) → Y5(R13-27 GATE)
```

- The three repos can progress in parallel lanes; the only hard cross-repo edges are: **W4 needs Y1 (host edit/settings/legend messages)** and **W3/W4 need the backend B1–B3 endpoints**.
- Density (W1) and navbar (W2) are independent and safe to land first.

## 5. Governance & lesser-agent execution

- One issue at a time per repo. For each issue: branch `feature/<n>-<slug>` (or `fix/`, `chore/`, `docs/`) from `develop` → implement smallest coherent change → verify → PR into `develop` → close the issue with a completion note (what changed, evidence) → merge → return repo to `develop` before the next issue (GOV-02).
- Verification bar = build + lint + targeted unit tests + a manual UI-check note. Full live end-to-end is deferred to the per-repo acceptance issues (R13-08 backend verification, R13-19 widget review, R13-27 yaml-widget review), which are **operator gates**.
- Each executor reads the relevant epic section of the matching issue index before starting; TypeDB/schema work must follow `.cursor/skills/typedb/SKILL.md`.
- Do not introduce `project_yaml`; do not fake data; latest emitted YAML wins.

## 6. Traceability

Requirement IDs `R13-01`…`R13-27`. GitHub epics/issues tagged `[SPEC-013]` in each repo; the three issue-index docs hold the ID → epic → issue → status map. Milestone "done" = the operator can start the API, open Projects (5 seeded rows, resilient on API down), double-click into the Composer, pick projects from the dropdown, add a new project, edit the workflow with pencil/gear, have edits persist to TypeDB, with the navbar auto-hiding and the DAG rendering correctly at partial width.
