# SPEC-017 A5 — Run-until-reset contract

**Issue:** [#1271](https://github.com/brettforbes/spiderfeet/issues/1271)  
**Correction:** [#1283](https://github.com/brettforbes/spiderfeet/issues/1283) — target temp on Run/Scan Now only

## Host rules (authoritative for B4)

1. After a workflow run reaches a **terminal** `run_state` (`SUCCESS` / `ERROR` / `CANCELLED` / equivalent), keep **Run Workflow** disabled.
2. **Reset Workflow** (`POST /api/v1/workflows/{id}/reset`) is the only path that re-enables Run.
3. Reset response includes:
   - `status: "RESET"`
   - `run_ready: true` — host may re-enable Run after a successful reset
   - `temporary_subgraph_id: null` — Reset does **not** re-seed a target temp
   - `target_seed: null`

## Backend rules

- Run Workflow / Scan Now **must not** wipe temporary subgraphs (A4).
- At the **start** of live `run_workflow` or `run_single_step`, ensure `target_context` + `scan_name=target` temporary_subgraph (R17-03). Idempotent.
- Project open / `GET …/complete` must **not** create the target temp.
- Reset **deletes all** project `temporary_subgraph` rows and rematerializes scan shells; it does **not** re-seed target temp.
- Client `PUT .../contexts/temporary` is a no-op (engine-owned writes).

## Viewer

- On Run Workflow / Scan Now start: re-GET temp list so the target subgraph appears with the DAG Target colour change.
- After Reset success: clear Temporary Subgraph Viewer (empty until next Run / Scan Now).
