# SPEC-001 — Governance Bootstrap & Module Taxonomy

**Status:** Active (bootstrap phase)  
**Type:** Bootstrap / governance setup spec  
**Created:** 2026-05-23

## Purpose

Establish VibeGov governance, Git workflow scaffolding, and a durable module taxonomy before any product-code implementation in this Spiderfeet fork.

## Scope

### In scope

- VibeGov `.governance/` scaffold (rules, project, specs)
- Module classification: OSINT services, quarantined modules, core non-OSINT
- Analysis tooling under `.docs/analysis/` (read-only extraction scripts)
- Reference documentation under `.docs/`
- GitHub preflight and board setup (or documented blockers)
- Continuity and checkpoint operating guidance

### Out of scope

- Spiderfeet runtime feature changes
- New scan modules or module rewrites
- UI / force-graph product implementation
- CI pipeline changes unless required for governance verification

## Requirements

### R1 — Governance scaffold

- [x] `.governance/rules/` contains GOV-01 through GOV-09
- [x] Rules mirrored to `.cursor/rules/` (provider-native rules directory detected)
- [x] `PROJECT_INTENT.md` exists and marked provisional where appropriate

### R2 — Module taxonomy

- [x] OSINT services extracted to `.docs/analysis/osint_services.json` (177 modules with `dataSource`)
- [x] Quarantined modules documented in `.docs/quarantine_modules.md` (54 modules pending verification)
- [x] Core non-OSINT documented in `.docs/non_osint_modules.md` (2 storage modules only)

### R3 — Git & delivery workflow

- [x] `AGENTS.md`, `INIT-TODO.md`, PR template, branch-protection checklist
- [x] Documented default issue-pickup / work-pickup flow
- [x] Local `develop` branch created for strict workflow (remote/protection reported separately)

### R4 — GitHub integration

- [x] Preflight recorded with explicit states
- [ ] Canonical project board adopted/created/normalized **or** blocker documented in `INIT-TODO.md`
- [ ] Repo linked to board when write access available

### R5 — Continuity

- [x] Continuity layers documented with repo-local paths
- [x] Checkpoint triggers and promotion guidance installed
- [x] Session diary template available

### R6 — Bootstrap reporting

- [x] Current surface: `.governance/project/bootstrap/{STATUS,ANALYSIS,FEEDBACK,BLOCKERS}.md`
- [x] Historical run bundle under `bootstrap/history/<run-id>/`

## Acceptance criteria

Bootstrap init is complete when Pass Gate #1 from [VibeGov Bootstrap](https://vibegov.io/docs/bootstrap) is satisfied and no product code was written during the bootstrap run.

## Traceability

| Section | Backlog IDs |
|---------|-------------|
| R1 | BL-001 |
| R2 | BL-002, BL-003, BL-004 |
| R3 | BL-005 |
| R4 | BL-006 |
| R5 | BL-007 |
| R6 | BL-008 |
