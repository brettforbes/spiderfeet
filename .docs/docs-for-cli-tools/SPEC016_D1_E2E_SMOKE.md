# SPEC-016 D1 — Cross-repo E2E smoke evidence

**Date:** 2026-08-10  
**Issue:** [#1259](https://github.com/brettforbes/spiderfeet/issues/1259) (R16-12)  
**Spec:** `.governance/specs/SPEC-016-workflow-run-robustness-and-per-project-context.md`

## Delivery landed (all three repos)

| Lane | Stories | Merged PRs (examples) |
|------|---------|------------------------|
| Backend A | A1–A4 | [#1261](https://github.com/brettforbes/spiderfeet/pull/1261) timeouts, [#1262](https://github.com/brettforbes/spiderfeet/pull/1262) non-blocking export, [#1263](https://github.com/brettforbes/spiderfeet/pull/1263) canonical context ids, [#1264](https://github.com/brettforbes/spiderfeet/pull/1264) seed timeout tests |
| YAML widget C | C1–C3 | [#271](https://github.com/brettforbes/yaml-workflow-widget/pull/271) target context port, [#272](https://github.com/brettforbes/yaml-workflow-widget/pull/272) target collector, [#273](https://github.com/brettforbes/yaml-workflow-widget/pull/273) layout docs |
| Host widget B | B1–B4 | [#252](https://github.com/brettforbes/spiderfeet-widget/pull/252) incremental import, [#253](https://github.com/brettforbes/spiderfeet-widget/pull/253) clustering, [#254](https://github.com/brettforbes/spiderfeet-widget/pull/254) per-project reload, [#255](https://github.com/brettforbes/spiderfeet-widget/pull/255) label centring |

## Automated evidence

- Seed timeouts present: nuclei=900, katana=600, nerva=300 (`12A_Workflow_YAML_Example.yaml`).
- Canonical temp ids distinct per project (`temporary_subgraph_id_for`).
- pytest: `test_seed_step_timeouts.py` + temporary-context isolation/coercion tests → **passed**.

## Live UI checklist (operator / D2)

Restart API + widget + yaml-workflow-widget from `develop`, then on k2am:

1. Run Workflow — nuclei must not abort at 180s; expect FINISHED or a longer honest timeout (≥900s wall).
2. Temporary Subgraph Viewer fills as each step hits FINISHED (not only at run end).
3. Project dropdown switch clears/reloads temp context; switch back restores.
4. DAG Target shows right-edge context port + `__ctxcol_target__` collector to the right.
5. Import chips cluster; clicking a chip centres that import.

## Residual

- Full interactive UI pass is **D2 operator gate** ([#1260](https://github.com/brettforbes/spiderfeet/issues/1260)).
- After A1 reseed, k2am step shells were rematerialized as `UNKNOWN` (expected); a fresh Run Workflow is required for live status colours.
