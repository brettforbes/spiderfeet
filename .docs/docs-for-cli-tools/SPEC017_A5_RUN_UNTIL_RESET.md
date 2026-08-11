# SPEC-017 A5 — Run-until-reset contract

**Issue:** [#1271](https://github.com/brettforbes/spiderfeet/issues/1271)

## Host rules (authoritative for B4)

1. After a workflow run reaches a **terminal** `run_state` (`SUCCESS` / `ERROR` / `CANCELLED` / equivalent), keep **Run Workflow** disabled.
2. **Reset Workflow** (`POST /api/v1/workflows/{id}/reset`) is the only path that re-enables Run.
3. Reset response includes:
   - `status: "RESET"`
   - `run_ready: true` — host may re-enable Run after a successful reset
   - `temporary_subgraph_id` — id of re-seeded `scan_name=target` temp when present
   - `target_seed` — ensure payload from `ensure_project_target_temps`

## Backend rules

- Run Workflow **must not** wipe temporary subgraphs (A4).
- Reset **deletes all** project `temporary_subgraph` rows, rematerializes scan shells, then re-seeds target temp.
- Client `PUT .../contexts/temporary` is a no-op (engine-owned writes).

## Viewer

After Reset success, host clears the Temporary Subgraph Viewer and `GET .../contexts/temporary` (list) to show target-only.
