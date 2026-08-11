# SPEC-017 D1 — Cross-repo E2E smoke evidence

**Date:** 2026-08-12  
**Issue:** [#1274](https://github.com/brettforbes/spiderfeet/issues/1274) (R17-14)  
**Spec:** `.governance/specs/SPEC-017-multi-temporary-subgraphs-and-dag-colors.md`

## Delivery landed (all three repos)

| Lane | Stories | Merged PRs |
|------|---------|------------|
| Backend A | A1–A6 | [#1276](https://github.com/brettforbes/spiderfeet/pull/1276) schema, [#1277](https://github.com/brettforbes/spiderfeet/pull/1277) per-export write, [#1278](https://github.com/brettforbes/spiderfeet/pull/1278) target + list API, [#1279](https://github.com/brettforbes/spiderfeet/pull/1279) run-until-reset + tests, [#1280](https://github.com/brettforbes/spiderfeet/pull/1280) ensure fixture fix |
| Host widget B | B1–B4 | [#261](https://github.com/brettforbes/spiderfeet-widget/pull/261)/[#262](https://github.com/brettforbes/spiderfeet-widget/pull/262) list load, [#263](https://github.com/brettforbes/spiderfeet-widget/pull/263) FINISHED reload, `cef3d63` cluster icon, [#264](https://github.com/brettforbes/spiderfeet-widget/pull/264)/[#265](https://github.com/brettforbes/spiderfeet-widget/pull/265) Run-until-Reset |
| YAML widget C | C1–C3 | [#278](https://github.com/brettforbes/yaml-workflow-widget/pull/278) status hex, [#279](https://github.com/brettforbes/yaml-workflow-widget/pull/279) edge colors, [#280](https://github.com/brettforbes/yaml-workflow-widget/pull/280) docs + smoke |

## Automated evidence (2026-08-12)

### Backend (`develop`)

| Check | Result |
|-------|--------|
| `pytest spiderfeet_v2/engine/tests/test_ensure_target_temps.py` | **4 passed** |
| `pytest …/test_v2_routes.py -k "temporary or ensure or reset or isolat"` | **5 passed** (includes `test_temporary_context_list_and_put_noop`, per-project isolation) |
| Contract note | `.docs/docs-for-cli-tools/SPEC017_A5_RUN_UNTIL_RESET.md` — `run_ready: true` on reset |

Verified behaviours in tests:

1. `GET /api/v1/projects/{id}/contexts/temporary` → `{ project_id, subgraphs: [...] }` with stamped `temporary_id` / `scan_name`.
2. `PUT .../contexts/temporary` is a **no-op** (returns list; does not replace engine-owned rows).
3. Ensure path seeds `scan_name=target` into a project temporary subgraph.
4. Reset wipes temps and reseeds target (`run_ready: true`).

### YAML widget (`develop`)

| Check | Result |
|-------|--------|
| `node src/workflow-dag/edgeColors.smoke.mjs` | **OK** (defaults include `#156082` / `#E97132` / `#78206E`) |
| `node src/workflow-dag/statusColors.smoke.mjs` | **STATUS_COLORS_SMOKE_OK** (`#FFFF99` / `#F2AA84` / `#4E95D9` / `#FF7979`) |

### Host widget (`develop`)

Code-path smoke (merged on develop; interactive UI = D2):

- `SpiderfeetApi.getTemporaryContexts` normalizes `subgraphs[]` (R17-07).
- `ComposerTempGraph` read-only list load; chips centre-only (R17-07).
- Status poller reloads temps on FINISHED (R17-08).
- `Composer._runBlockedUntilReset` gates Run until Reset succeeds (R17-10).

## Live UI checklist (operator / D2)

Restart API + widget + yaml-workflow-widget from **`develop`** (schema reload per `SPEC017_A1_SCHEMA_RELOAD.md` if TypeDB still has the old schema), then on a seeded project (e.g. k2am):

1. **Project open** → Temporary Subgraph Viewer shows target (`scan_name=target`) before any scan.
2. **Run Workflow** → each exporting step FINISHED grows `GET …/contexts/temporary` `subgraphs[]` (viewer reloads; no client PUT as source of truth).
3. **Chip click** centres that subgraph; **no delete** control on chips.
4. **Cluster icon** packs subgraphs with small separation.
5. After terminal run → **Run stays disabled** until **Reset Workflow**.
6. **Reset** wipes temps, reseeds target, returns `run_ready: true`, Run re-enabled.
7. YAML Settings → status + edge colors show picker **and** hex; defaults match SPEC-017 table (both themes).

## Residual

- Full interactive UI / GOV-08 matrix is **D2 operator gate** ([#1275](https://github.com/brettforbes/spiderfeet/issues/1275)).
- Live API was not reachable on `127.0.0.1:8001` during this D1 pass (timeout); restart required before D2.
