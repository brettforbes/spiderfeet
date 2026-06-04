# Agent Entrypoint — spiderfeet

Governed Spiderfeet fork. Read this before doing substantive work.

## Canonical sources

| What | Where |
|------|--------|
| Project intent | `.governance/project/PROJECT_INTENT.md` |
| Active spec (bootstrap) | `.governance/specs/SPEC-001-governance-bootstrap.md` |
| Active spec (product) | `.governance/specs/SPEC-002-first-four-stages.md` |
| Project rules | `.governance/project/rules/` (mirrored in `.cursor/rules/proj-*.mdc`) |
| Stage plan | `.seed/02_stage_by_stage_reengineer.md` |
| Backlog | `.governance/project/BACKLOG.md` |
| Governance rules | `.governance/rules/gov-*.mdc` (mirrored in `.cursor/rules/`) |
| Bootstrap status | `.governance/project/bootstrap/STATUS.md` |
| Setup blockers | `INIT-TODO.md` |
| Git workflow | `.governance/project/GIT_WORKFLOW.md` |
| Continuity | `.governance/project/continuity/README.md` |

## Module taxonomy docs

- OSINT services: `.docs/analysis/osint_services.json`
- Quarantined modules: `.docs/quarantine_modules.md`
- Core non-OSINT: `.docs/non_osint_modules.md`

## Operating rules

1. **Stage 0–4 work** must map to SPEC-002 requirement IDs (see `.governance/project/BACKLOG.md`).
2. Follow GOV-02 delivery loop: Observe → Plan → Implement → Verify → Document.
3. Issue-first / spec-first for implementation tasks (GOV-06).
4. Checkpoint continuity per GOV-09 when instructions change, blockers appear, or handoff risk is high.
5. **Commit policy:** only when the operator explicitly requests commits.

## Default work pickup

1. Check `INIT-TODO.md` and `.governance/project/bootstrap/BLOCKERS.md`.
2. Select backlog item from `.governance/project/BACKLOG.md` (or canonical GitHub board when available).
3. Confirm spec coverage; extend spec before coding.
4. Stop before product implementation if still in bootstrap phase.

## VibeGov bootstrap

- Contract: https://vibegov.io/docs/bootstrap
- This repo was bootstrapped in **`init`** mode on 2026-05-23.
