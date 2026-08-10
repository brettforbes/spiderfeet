# SPEC-015 D1 — Cross-repo E2E smoke evidence (R15-18)

**Date:** 2026-08-10  
**Issue:** [#1235](https://github.com/brettforbes/spiderfeet/issues/1235)  
**Repos on `develop`:** spiderfeet (Epic A), yaml-workflow-widget (Epic B), spiderfeet-widget (Epic C)

## Environment

| Service | URL / note | Verified |
|---------|------------|----------|
| FastAPI | `http://127.0.0.1:8001` — restarted after A1–A6 land (no reload) | health `ok`, OpenAPI includes async/status/reset |
| Host widget | `http://127.0.0.1:3000` webpack serve | HTTP 200 |
| YAML DAG widget | `http://127.0.0.1:4009/?embed=1` webpack serve | HTTP 200 |

## Contract smoke (API)

Project: `project--0c2f0994-df8b-538d-a9f1-e78d0afaf042`  
Workflow: `workflow--bffd4f87-b0e5-5e74-b5b9-11fefc6e3c7f`

1. **GET `/workflows/{id}/status`** — returned 6 steps with mixed `FINISHED` / `ERROR-FAILED` / `UNKNOWN`.
2. **POST `/workflows/{id}/execute-async`** (`dry_run: true`) — `202` with `run_id`; follow-up status showed `run_state: success`.
3. **POST `/workflows/{id}/reset`** — `steps_reset: 6`; subsequent status all `UNKNOWN`.

OpenAPI paths present after restart:

- `/api/v1/workflows/{workflow_id}/execute-async`
- `/api/v1/workflows/{workflow_id}/steps/{step_id}/execute-async`
- `/api/v1/workflows/{workflow_id}/status`
- `/api/v1/workflows/{workflow_id}/reset`

## UI readiness (operator exercise)

Hard-refresh Composer (`http://127.0.0.1:3000` → Composer tab). Confirm:

1. Status legend (⏱ ↻ ✓ ✕) next to Reset / Run Workflow.
2. Opening a project paints persisted step colors on the DAG (waiting/complete/failed).
3. **Run Workflow** — nodes move waiting → running → complete/failed live.
4. **Scan Now** on one step — that node pulses running then completes/fails.
5. **Reset Workflow** — DAG unwinds to waiting; temporary viewer clears.
6. Settings in the YAML iframe — status color pickers persist per light/dark theme.

## Delivery map

| Epic | PRs (merge to develop) |
|------|------------------------|
| A backend | #1237–#1242 |
| B yaml widget | #258–#262 |
| C host widget | #238–#243 |

## Note

D1 API smoke used **Reset** on the sample Venture Capital project workflow (cleared prior scan shells). Re-run Scan Now / Run Workflow to regenerate four forms if needed.

## Residual

- **D2** (#1236) — GOV-08 exploratory review — **operator gate** (not closed by this smoke).
