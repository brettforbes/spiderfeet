# SPEC-002 — First Four Stages (Spiderfeet v2)

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
| R2-01-01 | 1 | Complete SpiderFoot → Spiderfeet rebrand; Apache 2.0; operator selects logo |
| R2-02-01 | 2 | FastAPI exposes CLI-equivalent operations; Swagger + Requestly verification |
| R2-03-01 | 3 | TypeDB `spiderfeet-map` schema seed from `.seed/spiderfeet_map.tql` + analysis JSON |
| R2-03-02 | 3 | Map CRUD and force-graph export APIs |
| R2-03-03 | 3 | Widget Maps tab with D3 force graph; non-Maps tabs are empty placeholders |
| R2-04-01 | 4 | `scan-record` and `route` relations in map DB |
| R2-04-02 | 4 | Realistic test nugget corpus (AU, UK, US) |
| R2-04-03 | 4 | **One GitHub issue per OSINT module** (177); each issue covers all routes for that module (consumed×produced pairs exercised within the issue) |
| R2-04-04 | 4 | Widget Tests tab for running/viewing route tests and history |

## Stage 4 route testing

- **177 module-test issues** (one per entry in `osint_services.json`). Each issue tracks testing of all routes for that module (typically many consumed×produced combinations inside one issue).
- A module issue closes when all viable routes are exercised: `scan-record` per run, `route` on success, failures annotated per seed doc §2.4.3.
- Quarantine modules are **not** in this tranche; they follow in stage 5.

## Verification

- Development: pytest / npm build / Requestly / TypeDB bootstrap scripts per issue acceptance criteria.
- Exploratory: GOV-08 matrices on Maps and Tests tabs (issues SFW-03-18, SFW-04-09).

## Non-goals (this spec)

- Quarantine module conversion (stage 5)
- Favourites, sequences, Maltego-style investigation UI (stages 6–8)
