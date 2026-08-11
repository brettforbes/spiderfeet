# SPEC-017 issue index — backend (`spiderfeet`) + cross-repo

**Spec:** `.governance/specs/SPEC-017-multi-temporary-subgraphs-and-dag-colors.md`  
**Agent plan:** `.governance/project/SPEC017_AGENT_PLAN.md`  
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`  
**Skill (schema/DB):** `.cursor/skills/typedb/SKILL.md`

Status legend: `open` → `in progress` → `in review` → `done`.

## Cross-repo map

| Repo | Epic | Issue index |
|------|------|-------------|
| `spiderfeet` | A (multi temp TypeDB), D (integration) | this file |
| `spiderfeet-widget` | B (read-only viewer) | `@spiderfeet-widget/.governance/project/SPEC017_WIDGET_ISSUE_INDEX.md` |
| `yaml-workflow-widget` | C (DAG color settings) | `@yaml-workflow-widget/.governance/project/SPEC017_ISSUE_INDEX.md` |

## Epic A — Backend: multi temporary_subgraph (TypeDB-first)

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic A | [#1266](https://github.com/brettforbes/spiderfeet/issues/1266) | R17-01..06 | — | open |
| A1 — Schema repair | [#1267](https://github.com/brettforbes/spiderfeet/issues/1267) | R17-01 | — | open |
| A2 — Per-export temporary_subgraph write | [#1268](https://github.com/brettforbes/spiderfeet/issues/1268) | R17-02 | A1 | open |
| A3 — Target materialize | [#1269](https://github.com/brettforbes/spiderfeet/issues/1269) | R17-03 | A1 | open |
| A4 — List API + reset wipe/reseed | [#1270](https://github.com/brettforbes/spiderfeet/issues/1270) | R17-04 | A2, A3 | open |
| A5 — Run-until-reset contract | [#1271](https://github.com/brettforbes/spiderfeet/issues/1271) | R17-05 | A4 | open |
| A6 — Tests + OpenAPI | [#1272](https://github.com/brettforbes/spiderfeet/issues/1272) | R17-06 | A2–A5 | open |

## Epic D — Integration + acceptance

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic D | [#1273](https://github.com/brettforbes/spiderfeet/issues/1273) | R17-14..15 | A,B,C | open |
| D1 — Cross-repo E2E smoke | [#1274](https://github.com/brettforbes/spiderfeet/issues/1274) | R17-14 | A6, B*, C3 | open |
| D2 — GOV-08 exploratory [OPERATOR GATE] | [#1275](https://github.com/brettforbes/spiderfeet/issues/1275) | R17-15 | D1 | open |

## Execution order

```
A1 → A2 ∥ A3 → A4 → A5 → A6
D1 (needs A6 + B* + C3) → D2 (OPERATOR GATE)
```

**Unblocks host B1:** A4 merged to `develop`.

## Key files (backend)

- `.seed/spiderfeet_v2_semantic.tql` — temporary_subgraph / target_context (A1)
- `spiderfeet_v2/engine/persist.py` — write/reset temps (A2, A4)
- `spiderfeet_v2/engine/step_runner.py` — non-blocking export (A2)
- `spiderfeet_v2/api/routes/contexts.py` — list API; deprecate PUT (A4)
- `spiderfeet_v2/api/schemas.py` — OpenAPI (A4, A6)

## Governance

Branch from `develop`; PR into `develop`; one issue at a time; close with evidence; return to `develop` before next.
