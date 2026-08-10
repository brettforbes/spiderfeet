# SPEC-016 issue index — backend (`spiderfeet`) + cross-repo

**Spec:** `.governance/specs/SPEC-016-workflow-run-robustness-and-per-project-context.md`
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`
**Skill (schema/DB work):** `.cursor/skills/typedb/SKILL.md`

Status legend: `open` (created) → `in progress` → `in review` → `done`.

## Cross-repo map

| Repo | Epic | Issue index |
|------|------|-------------|
| `spiderfeet` | A (backend run robustness + per-project context), D (integration) | this file |
| `spiderfeet-widget` | B (host per-project reload + incremental import + viewer UX) | `@spiderfeet-widget/.governance/project/SPEC016_WIDGET_ISSUE_INDEX.md` |
| `yaml-workflow-widget` | C (target context port + collector) | `@yaml-workflow-widget/.governance/project/SPEC016_ISSUE_INDEX.md` |

## Epic A — Backend: run robustness + per-project context

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic A | [#1253](https://github.com/brettforbes/spiderfeet/issues/1253) | R16-01..04 | — | done |
| A1 — Per-step nuclei timeout (seed + module default) | [#1254](https://github.com/brettforbes/spiderfeet/issues/1254) | R16-01 | — | done |
| A2 — Non-blocking temporary-context export | [#1255](https://github.com/brettforbes/spiderfeet/issues/1255) | R16-02 | — | done |
| A3 — Per-project canonical context resolution + PUT hardening | [#1256](https://github.com/brettforbes/spiderfeet/issues/1256) | R16-03 | — | done |
| A4 — Backend tests, OpenAPI, docs | [#1257](https://github.com/brettforbes/spiderfeet/issues/1257) | R16-04 | A1..A3 | done |

## Epic D — Integration + acceptance (cross-repo)

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic D | [#1258](https://github.com/brettforbes/spiderfeet/issues/1258) | R16-12..13 | A,B,C | in progress |
| D1 — Cross-repo E2E smoke (k2am) | [#1259](https://github.com/brettforbes/spiderfeet/issues/1259) | R16-12 | A4,B*,C3 | done |
| D2 — GOV-08 exploratory review [OPERATOR GATE] | [#1260](https://github.com/brettforbes/spiderfeet/issues/1260) | R16-13 | D1 | open |

## Execution order

```
A1 (nuclei timeout) ∥ A2 (non-block export) ∥ A3 (per-project resolution) → A4 (tests/docs)
D1 (needs A4 + B* + C3) → D2 (OPERATOR GATE)
```

## Key files (backend)
- `.seed/12A_Workflow_YAML_Example.yaml` — nuclei step `timeout` (A1)
- `modules_v2/sfp_cli_nuclei.py` — module default 180→300 (A1, L381/L458)
- `spiderfeet_v2/engine/step_runner.py` — daemon-thread export (A2)
- `spiderfeet_v2/engine/persist.py` — `_write_temporary_context` best-effort (A2); `temporary_subgraph_id_for` (A3)
- `spiderfeet_v2/api/routes/contexts.py` — canonical id resolution + PUT hardening (A3)
- `spiderfeet_v2/api/tests/` — cross-project isolation tests (A4)

## Governance
Branch from `develop`; PR into `develop`; close each issue with a completion note + evidence; merge before the next. One issue at a time. Commit/merge per operator-approved policy.

## Contract notes (A4)

- Temporary context GET/PUT is per-project via `temporary_subgraph_id_for(project_id)`; PUT coerces foreign body ids.
- Seed `12A` long steps set `config.timeout` (nmap 900, nerva 300, katana 600, nuclei 900).

**D1 evidence:** .docs/docs-for-cli-tools/SPEC016_D1_E2E_SMOKE.md
