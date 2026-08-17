# SPEC-017 — `scan_name` schema outage (2026-08-12)

## Symptom

API logs: `[INF2] Type label 'scan_name' not found` on `list_subgraphs temporary` and `temporary_subgraph` inserts. Composer temporary viewer stayed empty; Run continued with “continuing without persist”.

## Cause

Long-lived `spiderfeet-actual` still had pre–SPEC-017 schema (`temporary_subgraph` only owned `temporary_subgraph_id`). Code expected `scan_name` / `scan_description` / `temporary_subgraph:scan_step`.

## Fix

1. Additive schema already present on live `spiderfeet-actual` (verified: attrs + owns + role).
2. `apply_spec017_schema_extensions()` in `spiderfeet_v2/db/bootstrap.py`, called from `bootstrap_actual` (existing DB path) and `ensure_actual_ready()` so API startup repairs this without G1 reset.
3. Docs: `.docs/docs-for-cli-tools/SPEC017_A1_SCHEMA_RELOAD.md`.

## Verify

- `GET …/contexts/temporary` returns `subgraphs[]` including `scan_name=target`.
- Operator: restart API to load bootstrap helper; **Reset Workflow** then **Run** for a clean stamped multi-temp set (legacy null-`scan_name` rows wipe on Reset).
