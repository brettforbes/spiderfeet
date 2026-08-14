# SPEC-018 issue index — backend (`spiderfeet`) + integration

**Spec:** `.governance/specs/SPEC-018-composer-refine.md`  
**Agent plan:** `.governance/project/SPEC018_AGENT_PLAN.md`  
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`

Status legend: `open` → `in progress` → `in review` → `done`.

## Cross-repo map

| Repo | Epic | Issue index |
|------|------|-------------|
| `spiderfeet` | A (GSE chain), B (persist + progress), E (integration) | this file |
| `spiderfeet-widget` | D (host Composer) | `@spiderfeet-widget/.governance/project/SPEC018_WIDGET_ISSUE_INDEX.md` |
| `yaml-workflow-widget` | C (DAG viz) | `@yaml-workflow-widget/.governance/project/SPEC018_ISSUE_INDEX.md` |

## Epic A — GSE proof + 12A chain

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic A | [#1285](https://github.com/brettforbes/spiderfeet/issues/1285) | R18-01..05 | — | done |
| A1 — Fixture proof matrix | [#1288](https://github.com/brettforbes/spiderfeet/issues/1288) | R18-01 | — | done |
| A2 — Fix GSE/YAML mismatches | [#1289](https://github.com/brettforbes/spiderfeet/issues/1289) | R18-02 | A1 | done |
| A3 — Nerva chain | [#1290](https://github.com/brettforbes/spiderfeet/issues/1290) | R18-03 | A2 | done |
| A4 — Nuclei chain | [#1291](https://github.com/brettforbes/spiderfeet/issues/1291) | R18-04 | A2 | done |
| A5 — GSE tests | [#1292](https://github.com/brettforbes/spiderfeet/issues/1292) | R18-05 | A2–A4 | done |

## Epic B — Persist-before-FINISHED + progress fields

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic B | [#1286](https://github.com/brettforbes/spiderfeet/issues/1286) | R18-06..08 | — | done |
| B1 — Persist temp before FINISHED | [#1293](https://github.com/brettforbes/spiderfeet/issues/1293) | R18-06 | — | done |
| B2 — Status input_total / input_done | [#1294](https://github.com/brettforbes/spiderfeet/issues/1294) | R18-07 | — | done |
| B3 — Tests + OpenAPI | [#1295](https://github.com/brettforbes/spiderfeet/issues/1295) | R18-08 | B1, B2 | done |

## Epic E — Integration + acceptance

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic E | [#1287](https://github.com/brettforbes/spiderfeet/issues/1287) | R18-18..19 | A,B,C,D | open (E2 operator gate) |
| E1 — Cross-repo E2E smoke | [#1296](https://github.com/brettforbes/spiderfeet/issues/1296) | R18-18 | A5, B3, C6, D* | done |
| E2 — GOV-08 exploratory [OPERATOR GATE] | [#1297](https://github.com/brettforbes/spiderfeet/issues/1297) | R18-19 | E1 | open |

## Execution order

```
A1 → A2 → A3 ∥ A4 → A5
B1 ∥ B2 → B3
E1 (needs A5 + B3 + YAML C6 + widget D*) → E2 (OPERATOR GATE)
```

## Key files (backend)

- `.seed/12A_Workflow_YAML_Example.yaml` — canonical workflow (A2)
- `.seed/12C_Graph_Select_Language.md` — GSE contract (A2)
- `spiderfeet_v2/workflow/gse_eval.py` — evaluator (A*)
- `spiderfeet_v2/engine/step_runner.py` — persist-before-FINISHED (B1)
- `spiderfeet_v2/engine/persist.py` — temp write + target dedupe (B1)
- `spiderfeet_v2/api/schemas.py` — `WorkflowStepStatusOut` (B2)
- `spiderfeet_v2/api/routes/execute.py` — status payload (B2)
- `.docs/docs-for-cli-tools/SPEC018_E1_E2E_SMOKE.md` — E1 evidence

## Governance

Branch from `develop`; PR into `develop`; one issue at a time; close with evidence; return to `develop` before next.
