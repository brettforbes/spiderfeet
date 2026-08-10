# SPEC-015 issue index — backend (`spiderfeet`) + cross-repo

**Spec:** `.governance/specs/SPEC-015-workflow-live-status-viz.md`
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`
**Skill (schema/DB work):** `.cursor/skills/typedb/SKILL.md`

Status legend: `open` (created) → `in progress` → `in review` → `done`.

## Cross-repo map

| Repo | Epic | Issue index |
|------|------|-------------|
| `spiderfeet` | A (backend async + status), D (integration) | this file |
| `yaml-workflow-widget` | B (DAG status rendering + colors) | `@yaml-workflow-widget/.governance/project/SPEC015_ISSUE_INDEX.md` |
| `spiderfeet-widget` | C (host poll + forward + unwind) | `@spiderfeet-widget/.governance/project/SPEC015_WIDGET_ISSUE_INDEX.md` |

## Epic A — Backend: async execution + live status API

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic A | [#1227](https://github.com/brettforbes/spiderfeet/issues/1227) | R15-01..06 | — | open |
| A1 — Async full-workflow execute + run registry | [#1228](https://github.com/brettforbes/spiderfeet/issues/1228) | R15-01 | — | done |
| A2 — GET /workflows/{id}/status | [#1229](https://github.com/brettforbes/spiderfeet/issues/1229) | R15-02 | A1 | done |
| A3 — Async single-step execute (Scan Now) | [#1230](https://github.com/brettforbes/spiderfeet/issues/1230) | R15-03 | A1 | done |
| A4 — Cancellation + reset integration | [#1231](https://github.com/brettforbes/spiderfeet/issues/1231) | R15-04 | A1 | done |
| A5 — Stuck-RUNNING guard in step_runner | [#1232](https://github.com/brettforbes/spiderfeet/issues/1232) | R15-05 | — | done |
| A6 — Tests, OpenAPI, docs | [#1233](https://github.com/brettforbes/spiderfeet/issues/1233) | R15-06 | A1..A5 | done |

## Epic D — Integration + acceptance (cross-repo)

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic D | [#1234](https://github.com/brettforbes/spiderfeet/issues/1234) | R15-18..19 | A,B,C | open |
| D1 — Cross-repo E2E smoke (Run + Scan Now live) | [#1235](https://github.com/brettforbes/spiderfeet/issues/1235) | R15-18 | A6,B5,C6 | open |
| D2 — GOV-08 exploratory review [OPERATOR GATE] | [#1236](https://github.com/brettforbes/spiderfeet/issues/1236) | R15-19 | D1 | open |

## Execution order

```
A1 → A2 → A3 ; A4 (needs A1) ; A5 (independent) → A6 (needs A1..A5)
D1 (needs A6 + B5 + C6) → D2 (OPERATOR GATE)
```

## Key files (backend)
- `spiderfeet_v2/api/routes/execute.py` — new `execute-async`, step `execute-async`, `status` routes
- new `spiderfeet_v2/engine/run_registry.py` — in-memory registry + executor
- `spiderfeet_v2/engine/workflow_runner.py` — cancel check between steps
- `spiderfeet_v2/engine/step_runner.py` — stuck-RUNNING guard (A5)
- `spiderfeet_v2/engine/persist.py` — `reset_workflow_execution` cancels active run (A4)
- `spiderfeet_v2/db/crud.py` — thin `scan_status`-only read (A2)
- `spiderfeet_v2/api/schemas.py` — async + status response models
- `spiderfeet_v2/workflow/typedb_convert.py` — `scan_instance_id_for` (id derivation)

## Governance
Branch from `develop`; PR into `develop`; close each issue with a completion note + evidence; merge before the next. One issue at a time. Commit/merge per operator-approved policy.
