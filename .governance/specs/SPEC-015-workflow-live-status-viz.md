# SPEC-015 — Workflow live status visualization

**Status:** Draft (awaiting operator approval to start lesser-agent execution)
**Source:** Operator request (2026-08-10) — show what is running now and what is left to run on the YAML DSL Workflow diagram, driven by both **Scan Now** and **Run Workflow**, with reset unwinding progress, and themeable status colors for light + dark.

**Parents (extends, does not replace):**
- Backend engine — `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
- Composer/Projects widget UI — `.governance/specs/SPEC-011-composer-projects-ui.md`
- Projects & Composer refinement — `.governance/specs/SPEC-013-projects-composer-refinement.md`
- YAML DSL Workflow iFrame — `@yaml-workflow-widget/.governance/specs/SPEC-012-update-widget.md`

**Repos in scope (split delivery):**

| Repo | Role in this phase |
|------|--------------------|
| `spiderfeet` | Async (background) workflow + single-step execution; in-memory run registry; cheap `GET /workflows/{id}/status`; cancel-on-reset; stuck-RUNNING guard |
| `yaml-workflow-widget` | New `setStepStatuses` inbound message; per-node status shade + icon; theme status color tokens (light+dark); settings color pickers + persistence |
| `spiderfeet-widget` | Async API client; forward statuses to the iFrame; poll during Run Workflow and Scan Now; unwind on reset; paint persisted status on project open |

**Issue indexes:**
- Backend — `.governance/project/SPEC015_ISSUE_INDEX.md`
- Widget — `@spiderfeet-widget/.governance/project/SPEC015_WIDGET_ISSUE_INDEX.md`
- YAML widget — `@yaml-workflow-widget/.governance/project/SPEC015_ISSUE_INDEX.md`

---

## 0. Operator-confirmed decisions

1. **Modify all three repos** — including `yaml-workflow-widget` (this is the tracked contract-gap escalation the SPEC-011 non-goal allows). Node status rendering and the color settings must live in the DAG widget; the host cannot paint nodes because it has no node geometry.
2. **Live progress (not optimistic).** Execution runs in the background; the frontend polls per-step `scan_status` and updates the DAG so waiting / running / complete / failed are visible simultaneously and update live.
3. **Both triggers show progress** — Scan Now (single step) and Run Workflow (full workflow).
4. **Four states**, keyed by DSL step id:
   - `waiting` (not yet run) — pale shade
   - `running` (in progress) — mid shade, pulsing
   - `complete` (finished) — strong shade
   - `failed` — distinct (red)
   Waiting/running/complete are three shades of one hue; failed is distinct. An icon overlay (clock / spinner / check / x) accompanies color for colorblind clarity.
5. **Reset unwinds** all step status back to `waiting` and clears the temporary context (already SPEC-013/earlier); any in-flight background run is cancelled so it cannot repaint RUNNING on fresh shells.
6. **Status colors are settable per theme** (light and dark) in the DAG widget settings panel, persisted, with a reset-to-default control.

## 0.1 Status mapping (backend `scan_status` → UI state)

- `UNKNOWN` → **waiting**
- `STARTING` / `RUNNING` → **running**
- `FINISHED` → **complete** (a `SKIPPED` outcome persists as `FINISHED`; shown as complete)
- `ERROR-FAILED` → **failed**

Keying uses the DSL **step id** (e.g. `sfp_cli_nmap`), matching `mapper.js` CLI node ids and `findNodeById(stepId)` — not the `${id}__category` child ids.

## 0.2 Data flow

```
composer.js  --POST execute-async-->  FastAPI (background thread, own CrudStore)
composer.js  --GET /workflows/{id}/status (poll ~1s)-->  FastAPI  --[{step_id, scan_status}]-->  composer.js
composer.js  --setStepStatuses {stepId: state}-->  yaml-workflow-widget iframe (:4009)  --renders shade+icon-->
FastAPI background run  --writes scan_status STARTING/RUNNING/FINISHED/ERROR-FAILED-->  TypeDB (committed per step)
```

## 0.3 Grounding facts (verified during planning)

- DAG rendering is entirely inside `yaml-workflow-widget`; inbound messages dispatch in `App.vue onHostMessage` (~L733–841) via `hostProtocol.js HOST_MSG`. Selection highlight already flows App-level `selectedNodeIds` → `:selected` prop → `.wf-node-selected` CSS (`var(--wd-accent)`); status mirrors this path.
- Theme tokens are CSS vars in `src/workflow-dag/theme.css` under `[data-theme="light"]` / `[data-theme="dark"]`; theme persists via `theme.js` localStorage. Settings panel is inline in `App.vue` (standalone L9–54, embed L76–114); no Vuex — persistence is per-feature localStorage.
- Backend execution is synchronous today; sync `def` handlers. Stores open a fresh TypeDB driver per CRUD call (no shared long-lived connection), and each `scan_status` write commits synchronously (`step_runner.py` L337–344: `ensure_scan_step(STARTING)` then `update_scan_step(RUNNING)`; terminal via `persist_module_result`). A background thread with its own `CrudStore.connect(...)` can run while a poll reads committed status. No existing job/async infra in `spiderfeet_v2`.
- `scan_instance_id_for(workflow_id, step_id)` = `f"scan_step--{uuid5(DNS_NS, f'{workflow_id}:{step_id}')}"` (`workflow/typedb_convert.py`). Step ids enumerated from stored `workflow_yaml`.
- Correctness gap: after `RUNNING`, only `ModuleResolveError` is remapped to `ERROR-FAILED`; any other exception can leave a row stuck at `RUNNING`. A general guard is required so polling terminates.

## 1. Objective

Give the operator an at-a-glance, live view of workflow execution on the DAG: which steps are waiting, which is running now, which have completed, and which failed — for both single-step and full-workflow runs — with reset returning every step to waiting, and with status colors themeable per light/dark.

## 2. Non-goals

- Parallel step execution (waves still run sequentially within the background run).
- Multi-worker / cross-process durability of the run registry (single API worker assumed; per-step `scan_status` in TypeDB remains the durable source of truth).
- Changing what a scan produces (four forms, nugget graph, temporary context) — unchanged from SPEC-010/011/013.
- New OSINT modules or ontology changes.

---

## 3. Requirements

### Backend (`spiderfeet`) — Epic A

| ID | Requirement |
|----|-------------|
| R15-01 | Background full-workflow execution: `POST /workflows/{id}/execute-async` returns `202 {run_id, workflow_id}` and runs `run_workflow` on a dedicated thread/executor, each run creating its own `CrudStore.connect(load_connection_config())`. A module-level in-memory run registry tracks `run_id → {workflow_id, project_id, state (queued|running|success|error|cancelled), started_at, finished_at, error, cancel_flag}`. Existing synchronous `execute` is preserved. |
| R15-02 | `GET /workflows/{id}/status` returns `{workflow_id, run_id?, run_state?, steps:[{step_id, scan_instance_id, scan_status}]}`, enumerating step ids from stored `workflow_yaml` and reading only `scan_status` (thin CRUD read that does not load four-form blobs). Missing shell → `UNKNOWN`. |
| R15-03 | Background single-step execution for Scan Now: `POST /workflows/{id}/steps/{step_id}/execute-async` returns `202 {run_id}` and runs `run_single_step` on the executor with its own store; status observable via R15-02. Existing synchronous step execute preserved. |
| R15-04 | Cancellation + reset integration: the run registry supports cancel; `run_workflow` background driver checks the cancel flag between steps and stops cleanly (marks `cancelled`). `reset_workflow_execution` cancels the active run for that workflow (and waits/guards) before rematerializing `UNKNOWN` shells, so a run cannot repaint RUNNING after reset. |
| R15-05 | Stuck-RUNNING guard: wrap `runner(spec)` in `step_runner` so any unexpected exception (not only `ModuleResolveError`) persists `ERROR-FAILED` for that step before re-raising/returning, guaranteeing polling always reaches a terminal state. |
| R15-06 | Tests + OpenAPI + docs: async lifecycle (202 → poll → terminal), status endpoint shape, cancel-on-reset, stuck-RUNNING guard; OpenAPI includes the three new paths; route/system docs note the async + status contract. `poetry run pytest` green for the new tests. |

### YAML widget (`yaml-workflow-widget`) — Epic B

| ID | Requirement |
|----|-------------|
| R15-07 | New inbound message `setStepStatuses`: add `SET_STEP_STATUSES: "setStepStatuses"` to `hostProtocol.js`; handle in `App.vue onHostMessage` into a `stepStatuses = ref({})` map `{ "<stepId>": "waiting"|"running"|"complete"|"failed" }`; payload `{ statuses: {...} }` (replace-semantics; empty map clears). Preserve all existing messages. |
| R15-08 | Node status rendering: pass status into `CliAppNode` (App.vue node wiring) and apply a status class (`wf-step-status-*`) plus an icon overlay (clock/spinner/check/x). Running pulses. Style uses the theme tokens from R15-09. Selection highlight remains independent and composable. |
| R15-09 | Theme status color tokens: add `--wd-status-waiting|running|complete|failed` under both `[data-theme="light"]` and `[data-theme="dark"]` in `theme.css`, with sensible defaults (one hue in three shades + red for failed). |
| R15-10 | Settings color pickers: add per-theme color pickers for the four statuses to both settings panels; persist via a new `statusColors.js` localStorage entry (`{light:{...},dark:{...}}`); apply live by setting the CSS variables on `.dag-host` (no diagram remount); include a reset-to-default control. |
| R15-11 | Docs + smoke: update `HOST_PROTOCOL.md` and `EMBED_GUIDE.md` with `setStepStatuses` (payload + states); add `hostStepStatuses.smoke.mjs` following the existing host-smoke pattern. |

### Host widget (`spiderfeet-widget`) — Epic C

| ID | Requirement |
|----|-------------|
| R15-12 | API client (`spiderfeet-api.js`): `executeWorkflowAsync(workflowId, body)`, `executeStepAsync(workflowId, stepId, body)`, `getWorkflowStatus(workflowId)` (and cancel if backend exposes it), returning the SPEC-015 shapes. |
| R15-13 | Bridge (`composer-workflow.js`): `ComposerWorkflow.setStepStatuses(map)` → `postToWidget('setStepStatuses', { statuses })`; add the `HOST_MSG` constant; no-op safely before iframe `ready`. |
| R15-14 | Run Workflow live: `composer.js runWorkflow` starts the async run, polls `getWorkflowStatus` (~1s), maps `scan_status`→UI state (§0.1), forwards via `setStepStatuses`, and stops on terminal `run_state`; existing temporary-context import at completion is preserved. |
| R15-15 | Scan Now live: the CliScanApp step path (`_beforeCliScanExecute` / `_onCliScanComplete`) starts the single-step async run and polls+forwards that step's status until terminal. |
| R15-16 | Reset + project-switch: `resetWorkflow` stops the poller and pushes an all-`waiting`/cleared `setStepStatuses` so the DAG unwinds; on project open/restore, fetch status once and paint persisted states (completed steps show as complete). |
| R15-17 | Poller lifecycle: a single active poller, torn down on tab switch / panel unmount / new run, with error backoff; add a small status legend in the Composer chrome (waiting/running/complete/failed). |

### Integration + acceptance — Epic D

| ID | Requirement |
|----|-------------|
| R15-18 | Cross-repo E2E smoke: with API + widget + yaml widget running, Run Workflow shows live waiting→running→complete/failed on the DAG; Scan Now shows live status for one step; reset unwinds to waiting; evidence recorded (screenshots/notes). |
| R15-19 | GOV-08 exploratory review of the live status visualization: scenario matrix (happy full run, single step, failure step, reset unwind, project switch repaint, color settings persist in both themes, colorblind icon fallback, poller teardown) classified with tracked follow-ups. **[OPERATOR GATE]** |

---

## 4. Execution order & cross-repo dependencies

```
Backend:  A1 → A2 → A3 ; A4 (needs A1) ; A5 (independent) → A6 (needs A1..A5)
YAML:     B1 → B2 → B3 → B4 → B5
Host:     C1 (needs A1..A3) → C3 ; C2 (needs B1) → C3 ; C4 (needs A3,C2) ; C5 (needs A4,C2) ; C6 (needs C3)
Integr.:  D1 (needs A6,B5,C6) → D2 (OPERATOR GATE)
```

- Hard cross-repo edges: host **C1** needs backend **A1–A3**; host **C2/C3** need widget **B1**; **C5** needs backend **A4**.
- Unblockers to start first, in parallel lanes: backend **A1/A2** and widget **B1**.

## 5. Governance & lesser-agent execution

- One issue at a time per repo. For each issue: branch `feature/<n>-<slug>` (or `fix/`,`chore/`,`docs/`) from `develop` → smallest coherent change → verify → PR into `develop` → close issue with a completion note + evidence → merge → return repo to `develop` before the next (GOV-02).
- Verification bar = build + lint + targeted unit/smoke tests + a manual note. Full live end-to-end is deferred to Epic D (D1 smoke, D2 operator-gate review).
- Schema/DB work follows `.cursor/skills/typedb/SKILL.md`. YAML widget work integrates via the documented postMessage contract and updates `HOST_PROTOCOL.md`/`EMBED_GUIDE.md`.
- Commit/merge only per each repo's commit policy (operator-approved).

## 6. Traceability

Requirement IDs `R15-01`…`R15-19`. GitHub epics/issues tagged `[SPEC-015]` in each repo; the three issue-index docs hold the ID → epic → issue → status map. Milestone "done" = operator can start a workflow (Run Workflow or Scan Now) and watch steps move waiting→running→complete/failed live on the DAG, reset returns all steps to waiting, and status colors are configurable per light/dark theme and persist.
