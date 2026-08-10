# SPEC-015 — Async workflow execute + live status

**Spec:** `.governance/specs/SPEC-015-workflow-live-status-viz.md`  
**Issue index:** `.governance/project/SPEC015_ISSUE_INDEX.md`

## API contract (backend)

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/v1/workflows/{id}/execute-async` | Accept full-workflow run → **202** `{run_id, workflow_id, state}` |
| `POST` | `/api/v1/workflows/{id}/steps/{step_id}/execute-async` | Accept single-step run → **202** |
| `GET` | `/api/v1/workflows/{id}/status` | Per-step `{step_id, scan_instance_id, scan_status}` + optional `run_id` / `run_state` |
| `POST` | `/api/v1/workflows/{id}/reset` | Cancel in-flight run, rematerialize UNKNOWN shells, clear temporary context |

Synchronous `/execute` and `/steps/{id}/execute` are unchanged.

## Status mapping (for DAG UI)

| `scan_status` | UI state |
|---------------|----------|
| `UNKNOWN` | waiting |
| `STARTING` / `RUNNING` | running |
| `FINISHED` | complete |
| `ERROR-FAILED` | failed |

## Implementation notes

- Background jobs: `spiderfeet_v2/engine/run_registry.py` (thread pool; each job creates its own `CrudStore` via `store_factory`).
- Thin status read: `CrudStore.get_scan_status` (no four-form attrs).
- Cancel: `should_cancel` checked between steps; reset calls `cancel_workflow` first.
- Stuck-RUNNING guard: unexpected module exceptions persist `ERROR-FAILED` (R15-05).
