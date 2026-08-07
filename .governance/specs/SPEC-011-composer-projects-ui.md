# SPEC-011 — Composer & Projects widget UI (v2 engine)

**Status:** Active
**Parent coordination:** Source prompt `.seed/17_SpiderFeet_v2_Integrating_TypeDB_FastAPI_iFrame.md`; consumes the SPEC-010 v2 engine API
**Backend spec:** `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
**Plan / agent playbook:** `@spiderfeet-widget/.governance/project/SPEC011_AGENT_PLAN.md`
**Issue index (widget):** `@spiderfeet-widget/.governance/project/SPEC011_WIDGET_ISSUE_INDEX.md`
**Reused components:** `Widgets.CliScanApp` (SPEC-008), `Viz.CanvasGraph` (SPEC-009), `DataViewerHost` + `Theme` (data-viewer-embed)
**Embedded editor:** `yaml-workflow-widget` iframe (`http://localhost:4009/`), protocol `@spiderfeet-widget` data-viewer-embed pattern + `HOST_PROTOCOL.md`

## Objective

Deliver the **Projects page** (replacing the disabled *Enrichments* nav stub, renamed **Projects**) and the **Composer page** in `spiderfeet-widget`, wired to the SPEC-010 v2 engine on `http://127.0.0.1:8001/api/v1`.

- **Projects page:** table of projects with create/edit/delete; clicking a row pulls the full project JSON and routes to the Composer.
- **Composer page:** four coordinated visual elements —
  1. **Project Context Viewer** (upper split pane, `Viz.CanvasGraph`) — empty node/edge set in this spec (future project);
  2. **Temporary Subgraph Viewer** (lower split pane, `Viz.CanvasGraph`) — imports exported scan graphs as discrete subgraphs;
  3. **YAML DSL Workflow Editor** (collapsible left iframe embedding `yaml-workflow-widget`);
  4. **Simple CLI App Visualiser** (`Widgets.CliScanApp`, 5 tabs) sliding in from the right on step selection.

## Non-goals

- Backend engine, TypeDB, workflow runtime, execute API — that is **SPEC-010**.
- The Project Context Viewer's populated content / subgraph combine rules (kept empty here; future spec).
- Modifying the `yaml-workflow-widget` repo beyond host-side integration; its postMessage contract (`setYaml`/`getYaml`/`selectStep`/`stepSelected`/`setTheme`/`themeChanged`) is treated as complete. A concrete round-trip gap (option-edit → YAML update) is tracked as widget-host work (R11-14) and only escalates to a `yaml-workflow-widget` issue if the contract genuinely can't support it.
- Rebuilding `CliScanApp` or `CanvasGraph` (reused as-is; extended only where noted).

## Requirements

### Epic AQ — v2 API client + Projects page

| ID | Requirement |
|----|-------------|
| R11-01 | A v2 API client module (`src/js/spiderfeet-api.js` or similar) wraps the SPEC-010 routes (projects/workflows/targets/scan CRUD, execute, contexts) against `data-api-base` (`http://127.0.0.1:8001/api/v1`); errors surface as UI-visible states, not silent failures. |
| R11-02 | The **Enrichments** nav button is renamed **Projects**, enabled, and given a real pane (`#pane-projects`); shell wiring (`shell.js`) activates it. Maps/Tests/Subscriptions/CLI-Profiling/Settings are unchanged. |
| R11-03 | Projects page renders a table of projects (id, created, workflow count, stix incident id if present) from `GET /projects`; empty/loading/error states are handled. |
| R11-04 | Create / edit / delete project actions call the v2 API and reflect the result; a delete is verified by refresh (persistence proof, not toast-only). |
| R11-05 | Clicking a project row fetches the full project JSON and navigates to the Composer page with that project loaded (state passed in-app, re-fetchable on refresh). |

### Epic AR — Composer page shell (4-pane layout)

| ID | Requirement |
|----|-------------|
| R11-06 | The **Composer** nav button is enabled with a real pane (`#pane-composer`). Layout: a central area split horizontally into the Project Context Viewer (upper) and Temporary Subgraph Viewer (lower); a collapsible left column for the YAML editor iframe; a right slide-in region for `CliScanApp`. A 12-column model governs the left/right regions (see AS/AT). |
| R11-07 | Each of the two central panes has a full-screen expand icon (top-right) and, when expanded, a revert icon to return to the split size; expand/revert is keyboard-accessible. |
| R11-08 | Both central panes host `Viz.CanvasGraph` instances. The **Project Context Viewer** is initialized with an **empty** `{nodes:[], links:[]}` set (future content) and does not error on empty data. |

### Epic AS — Embed YAML Workflow Editor iframe

| ID | Requirement |
|----|-------------|
| R11-09 | A collapsing left container embeds the `yaml-workflow-widget` iframe (`http://localhost:4009/`, `?embed=1` viz-only by default). Three width states: **collapsed** (0 columns, on the left border), **partial** (≈3 columns, viz-only, the default), **full** (12 columns, code + viz); toggled by icons. |
| R11-10 | Host↔iframe handshake follows `HOST_PROTOCOL.md`: wait for `ready`, then `setTheme` + `setYaml`; the host loads the current workflow's YAML into the editor and listens for `yamlChanged`/`validationResult`. |
| R11-11 | Light/dark theme stays synchronized both ways (`Widgets.Theme` → `setTheme`; iframe `themeChanged` respected) so the embedded editor matches the host. |

### Epic AT — Step selection → CliScanApp slide-in

| ID | Requirement |
|----|-------------|
| R11-12 | When the editor emits `stepSelected {stepId}`, the correct per-tool `CliScanApp` slides in from the right covering columns 4–12; the tool viewer matches the step's `uses` tool. Special step ids (`__workflow_start__`, `__workflow_target__`, `__workflow_end__`, etc.) are handled gracefully (no crash; appropriate no-op or summary). |
| R11-13 | If the step has **not** been run, only the **Scan** tab is accessible with **Scan Now disabled**, while the rest of the option controls remain enabled so the user can select options. The other four tabs are locked until a run exists. |

### Epic AU — Option-edit round-trip + run gating

| ID | Requirement |
|----|-------------|
| R11-14 | Changes made to scan options in `CliScanApp` (Scan tab, edit-run) are sent to the YAML editor so the workflow YAML and its viz update to reflect the option changes (via `setYaml` with the recomputed YAML, or the editor's option-update message if available). Round-trip is demonstrated (change an option → YAML updates → viz updates). |
| R11-15 | Scan Now becomes enabled only when the step's four sub-tasks (Input, Config, Output, Context) are validly set — i.e. the editor reports the workflow YAML for that step as valid (`validationResult.ok`). The enable/disable transition is driven by messages from the editor, not guessed client-side. |

### Epic AV — Live execute + read-only replay

| ID | Requirement |
|----|-------------|
| R11-16 | With a valid step and Scan Now enabled, clicking Scan Now calls the SPEC-010 execute endpoint, shows progress, and on completion populates the Text / Structured / Graph / Report tabs from the returned four forms; the scan_step is persisted server-side (verified by re-fetch). |
| R11-17 | Selecting a step that has already been run loads its stored four forms in **read-only** mode (all five tabs viewable, Scan Now shown complete/disabled), sourced from the persisted scan_step. |
| R11-23 | With a multi-step workflow YAML that the YAML DSL Workflow iframe reports as valid (`validationResult.ok`), the Composer exposes a **Run Workflow** control that persists the current editor YAML to the workflow record, calls the SPEC-010 full-workflow execute endpoint (`POST /workflows/{workflow_id}/execute` / AO2), shows progress and a succeeded/failed/skipped summary, and imports each completed step whose `context.export` is `scan_graph` into the Temporary Subgraph Viewer as discrete subgraphs (same import rules as R11-18). Per-step Scan Now (R11-16) remains available and unchanged. Run Workflow stays disabled while validation is not `ok` or while a workflow run is in flight. |

### Epic AW — Temporary Subgraph Viewer behavior

| ID | Requirement |
|----|-------------|
| R11-18 | On a completed step whose `context.export` is `scan_graph`, the scan graph is imported into the Temporary Subgraph Viewer: each imported node gets a fresh `temporary_id` (`temporary--<uuidv4>`, using the shared id method), edges are remapped to the temporary ids, and the new nodes/edges are appended to the viewer as a **discrete** subgraph alongside prior imports (overlapping canonical ids do not collide). |
| R11-19 | The viewer renders the accumulated imports as a series of discrete subgraphs on the `Viz.CanvasGraph` canvas and provides a toggle to remove an imported subgraph. |
| R11-20 | When the temporary graph is sent back to the server, `temporary_id`s are stripped and edges are mapped back to the original `nugget_instance_id` values (round-trip: temporary ids exist only inside the viewer). This aligns with the SPEC-010 temporary-context update endpoint (R10-25). |

### Epic AX — Widget end-to-end acceptance

| ID | Requirement |
|----|-------------|
| R11-21 | Full Composer flow demonstrated against the live v2 engine for at least one of the 4 example targets: load a project → open Composer → select steps → set options (YAML updates) → run → see four forms → exported graphs accumulate in the Temporary Subgraph Viewer → temporary graph round-trips to the server. **[OPERATOR GATE — final acceptance sign-off, see plan §0.1]** |
| R11-22 | GOV-08 exploratory review of the Projects and Composer pages: scenario matrix (happy path, empty, loading, error, cancel/collapse, invalid options, keyboard, refresh persistence) classified `Validated`/`Invalidated`/`Blocked`/`Uncovered-spec-gap`, with tracked follow-ups for anything not `Validated`. |

## Milestone (what "done" looks like for the operator)

The renamed **Projects** tab lists projects; clicking one opens the **Composer**. The left YAML editor shows the workflow diagram (collapsible to 0 / 3 / 12 columns, theme-matched). Clicking a workflow step slides in that tool's 5-tab CLI app on the right; unset steps allow option editing with Scan Now disabled until the step's YAML is valid; setting options updates the workflow YAML/diagram. Running a single step (Scan Now) or a validated multi-step workflow (Run Workflow) shows Text/Structured/Graph/Report for steps as applicable and, when a step exports its scan graph, drops that subgraph into the lower Temporary Subgraph Viewer as a discrete graph. The upper Project Context Viewer is present but empty. The whole flow works live against the SPEC-010 engine for a real target.

## Architecture

```text
spiderfeet-widget/src/
  html/content.html         ← rename Enrichments→Projects; add #pane-projects, #pane-composer
  js/shell.js               ← enable Projects + Composer tabs
  js/spiderfeet-api.js      ← v2 engine API client (new)
  js/projects.js            ← Projects table + CRUD (new)
  js/composer.js            ← Composer layout, pane full-screen, region coordination (new)
  js/composer-workflow.js   ← yaml-workflow-widget iframe embed + postMessage bridge (new)
  js/composer-temp-graph.js ← Temporary Subgraph Viewer (temporary_id merge, discrete subgraphs) (new)
  js/cli-scan-app.js        ← reused (edit-run slide-in; option-edit → YAML message)
  js/canvas-graph.js        ← reused (both central viewers)
  js/theme.js / data-viewer-host.js ← reused (theme sync, structured pane)
```

## Traceability

Implementation: GitHub epics under `[SPEC-011]` in `brettforbes/spiderfeet-widget`. Epic letters `AQ`–`AX` (continuing after SPEC-010's `AH`–`AP`). Requirement IDs `R11-01`…`R11-22`. Depends on SPEC-010 API (Epic AN endpoints) for AV/AW/AX; AQ–AU can proceed against a documented API contract + local stubs.
