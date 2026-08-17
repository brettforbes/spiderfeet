# SPEC-019 issue index — backend (`spiderfeet`) + integration

**Spec:** `.governance/specs/SPEC-019-composer-refine-2.md`  
**Agent plan:** `.governance/project/SPEC019_AGENT_PLAN.md`  
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`

Status legend: `open` → `in progress` → `in review` → `done`.

## Cross-repo map

| Repo | Epic | Issue index |
|------|------|-------------|
| `spiderfeet` | A (identity+GSE), B (Nerva), C (Nuclei), F (hierarchy), E (integration) | this file |
| `yaml-workflow-widget` | D (collector deps + ports) | `@yaml-workflow-widget/.governance/project/SPEC019_ISSUE_INDEX.md` |
| `spiderfeet-widget` | — | **no SPEC-019 issues** |

## Epic A — Graph identity + host-scoped GSE

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic A | [#1308](https://github.com/brettforbes/spiderfeet/issues/1308) | R19-01..04 | — | open |
| A1 — uuid4 + parent cache + validate_graph | [#1309](https://github.com/brettforbes/spiderfeet/issues/1309) | R19-01 | — | open |
| A2 — topology parent_id | [#1310](https://github.com/brettforbes/spiderfeet/issues/1310) | R19-02 | A1 | open |
| A3 — host-scoped GSE ip_port_list | [#1311](https://github.com/brettforbes/spiderfeet/issues/1311) | R19-03 | A2 | open |
| A4 — identity/GSE docs | [#1312](https://github.com/brettforbes/spiderfeet/issues/1312) | R19-04 | A3 | open |

## Epic B — Nerva hydrate

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic B | [#1313](https://github.com/brettforbes/spiderfeet/issues/1313) | R19-05..06 | — | open |
| B1 — Hydrate --output / -o | [#1314](https://github.com/brettforbes/spiderfeet/issues/1314) | R19-05 | A1 | open |
| B2 — ip:port list fixture | [#1315](https://github.com/brettforbes/spiderfeet/issues/1315) | R19-06 | A3, B1 | open |

## Epic C — Nuclei batching

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic C | [#1316](https://github.com/brettforbes/spiderfeet/issues/1316) | R19-07..09 | — | open |
| C1 — Wire urls into existing batching | [#1317](https://github.com/brettforbes/spiderfeet/issues/1317) | R19-07 | — | open |
| C2 — Batch i/n + timeouts | [#1318](https://github.com/brettforbes/spiderfeet/issues/1318) | R19-08 | C1 | done |
| C3 — Tests + crawl_urls URL-only | [#1319](https://github.com/brettforbes/spiderfeet/issues/1319) | R19-09 | C2 | done |

## Epic F — Company / subdomain / URL hierarchy

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic F | [#1320](https://github.com/brettforbes/spiderfeet/issues/1320) | R19-15..22 | — | open |
| F1 — Catalogue COMPANY/SUBDOMAIN + COMPANY_NAME retype | [#1321](https://github.com/brettforbes/spiderfeet/issues/1321) | R19-15 | — | open |
| F2 — add_company_domain_tree helper | [#1322](https://github.com/brettforbes/spiderfeet/issues/1322) | R19-16 | A1, F1 | open |
| F3 — Subfinder adapter + 12A GSE | [#1323](https://github.com/brettforbes/spiderfeet/issues/1323) | R19-17 | F2 | open |
| F4 — HTTPX website root + HTTP_STATUS_CODE | [#1324](https://github.com/brettforbes/spiderfeet/issues/1324) | R19-18 | F2 | open |
| F5 — Katana hostname URL ownership | [#1325](https://github.com/brettforbes/spiderfeet/issues/1325) | R19-19 | F2 | open |
| F6 — Pius COMPANY wrap | [#1326](https://github.com/brettforbes/spiderfeet/issues/1326) | R19-20 | F2 | open |
| F7 — Nerva apex COMPANY wrap | [#1327](https://github.com/brettforbes/spiderfeet/issues/1327) | R19-21 | F2 | open |
| F8 — Validator + synthetic tests | [#1328](https://github.com/brettforbes/spiderfeet/issues/1328) | R19-22 | F3–F7 | done |

## Epic E — Integration + acceptance

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic E | [#1329](https://github.com/brettforbes/spiderfeet/issues/1329) | R19-13..14 | A,B,C,D,F | open |
| E1 — Cross-repo E2E smoke | [#1330](https://github.com/brettforbes/spiderfeet/issues/1330) | R19-13 | A3, B2, C3, D3, F8 | done |
| E2 — GOV-08 exploratory [OPERATOR GATE] | [#1331](https://github.com/brettforbes/spiderfeet/issues/1331) | R19-14 | E1 | open |

## Execution order

```
A1 → A2 → A3 → A4
F1 ∥ A1
F2 after A1+F1
F3–F7 after F2 (parallel)
F8 after F3–F7
B1 after A1; B2 after A3
C1 ∥ C2 → C3
E1 after A3+B2+C3+YAML D3+F8 → E2 (OPERATOR GATE)
```

## Key files (backend)

- `modules_v2/_core/graph_builder.py` and `.seed/scripts/cli_corpus/core/graph_builder.py` (A1)
- `modules_v2/_core/topology.py` and `.seed/scripts/cli_corpus/core/topology.py` (A2, F2)
- `spiderfeet_v2/workflow/gse_eval.py` and `.seed/12A_Workflow_YAML_Example.yaml` (A3, F3, C3)
- `modules_v2/sfp_cli_nerva.py` / nerva adapter (B1, F7)
- `modules_v2/sfp_cli_nuclei.py` and `spiderfeet_v2/engine/step_runner.py` (C*)
- `modules_v2/adapters/{subfinder,httpx,katana,pius,nerva}/hooks.py` (F3–F7)
- `.docs/analysis/nuggets.json` + `nuggets_extension.json` and `modules_v2/_catalogues/` copies (F1)
- `.docs/docs-for-cli-tools/SPEC019_E1_E2E_SMOKE.md` (E1)

## Governance

Branch from `develop`; PR into `develop`; one issue at a time; close with evidence; return to `develop` before next.

