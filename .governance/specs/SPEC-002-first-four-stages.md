# SPEC-002 — First Four Stages (SpiderFeet v2)

**Status:** Approved 2026-06-03  
**Source:** `.seed/02_stage_by_stage_reengineer.md`  
**Planning:** `.seed/planning/FIRST_FOUR_STAGES_EPICS_AND_ISSUES.md`  
**Issue manifest:** `.seed/planning/github_issues_manifest.json`

## Scope

Stages 0–4 only (governance → rebrand → FastAPI → TypeDB map UI → per-route module testing). Stages 5–8 (quarantine, favourites, storage, main UI) are explicitly out of scope.

## Requirements

| ID | Stage | Requirement |
|----|-------|-------------|
| R2-00-01 | 0 | Project-specific governance rules in both roots, mirrored to `.cursor/rules/` |
| R2-00-02 | 0 | SPEC-002 traceability; unified GitHub Project for both repos |
| R2-01-01 | 1 | Complete SpiderFeet → SpiderFeet rebrand; Apache 2.0; operator selects logo |
| R2-02-01 | 2 | FastAPI exposes CLI-equivalent operations; Swagger + Requestly verification |
| R2-02-01a | 2 | CLI capability matrix documented in `.docs/api/cli_capability_matrix.md` |
| R2-02-01b | 2 | FastAPI skeleton: `/api/v1/health`, CORS, `start.ps1 -Mode api` |
| R2-03-01 | 3 | TypeDB `spiderFeet-map` schema seed from `.seed/spiderFeet_map.tql` + analysis JSON |
| R2-03-02 | 3 | Map CRUD and force-graph export APIs |
| R2-03-03 | 3 | Widget Maps tab with D3 force graph; non-Maps tabs are empty placeholders |
| R2-04-01 | 4 | `scan-record` and `route` relations in map DB |
| R2-04-02 | 4 | Realistic test nugget corpus (`test_nugget_data.csv` + validation script) |
| R2-04-03 | 4 | **One GitHub issue per OSINT module** (177); each issue covers all routes for that module (consumed×produced pairs exercised within the issue) |
| R2-04-04 | 4 | Widget Tests tab for running/viewing route tests and history |
| R2-04-05 | 4 | **SPEC_GAP** — Subscriptions page: per-module API key CRUD (masked) |
| R2-04-06 | 4 | **SPEC_GAP** — Subscription tiers (`none` / `free_auth` / `paid_auth`); gate Tests visibility |
| R2-04-07 | 4 | Module-validated test corpus (`module_test_seeds.json`; pilot 10 none-tier modules) |
| R2-04-08 | 4 | Strict test pass: **positive** — `FINISHED` + produced objects; **negative** — `FINISHED` + `module_execution.verdict = clean_miss` (and `expected_absent_types` absent). `fixture_category` on TypeDB `osint-service`; dual seeds (`positive_hit` for dirty tuning); `GET /scans/{id}/logs` |
| R2-04-09 | 4 | `service_state` on catalogue + TypeDB `osint-service` (`in-test` default; `error` for upstream-broken modules). Tests and Subscriptions APIs exclude `error`; Maps may still show until filter added. Sync: `sync_service_state.py` |

## Stage 4 route testing

- **177 module-test issues** (one per entry in `osint_services.json`). Each issue tracks testing of all routes for that module (typically many consumed×produced combinations inside one issue).
- A module issue closes when all viable routes are exercised: `scan-record` per run, `route` on success, failures annotated per seed doc §2.4.3.
- Quarantine modules are **not** in this tranche; they follow in stage 5.
- None-tier free modules: seed research closed (79 smoke-validated, 8 `service_state: error`). See `.docs/analysis/stage4_seed_corpus_and_tests.md`.

## Verification

- Development: pytest / npm build / Requestly / TypeDB bootstrap scripts per issue acceptance criteria.
- Exploratory: GOV-08 matrices on Maps and Tests tabs (issues SFW-03-18, SFW-04-09).

## Non-goals (this spec)

- Quarantine module conversion (stage 5)
- Favourites, sequences, Maltego-style investigation UI (stages 6–8)
