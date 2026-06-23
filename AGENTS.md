# Agent Entrypoint — spiderFeet

Governed SpiderFeet fork. Read this before doing substantive work.

## Canonical sources

| What | Where |
|------|--------|
| Project intent | `.governance/project/PROJECT_INTENT.md` |
| Active spec (bootstrap) | `.governance/specs/SPEC-001-governance-bootstrap.md` |
| Active spec (product) | `.governance/specs/SPEC-002-first-four-stages.md` |
| Active spec (stage 5) | `.governance/specs/SPEC-003-stage5-quarantine.md` |
| Project rules | `.governance/project/rules/` (mirrored in `.cursor/rules/proj-*.mdc`) |
| Stage plan | `.seed/02_stage_by_stage_reengineer.md` |
| Backlog | `.governance/project/BACKLOG.md` |
| Governance rules | `.governance/rules/gov-*.mdc` (mirrored in `.cursor/rules/`) |
| Bootstrap status | `.governance/project/bootstrap/STATUS.md` |
| Setup blockers | `INIT-TODO.md` |
| Git workflow | `.governance/project/GIT_WORKFLOW.md` |
| Continuity | `.governance/project/continuity/README.md` |

## Module taxonomy docs

- OSINT services: `.docs/analysis/osint_services.json` (`service_state`, `fixture_category`)
- Quarantined modules: `.docs/quarantine_modules.md`
- Core non-OSINT: `.docs/non_osint_modules.md`
- **Nugget ontology (canonical):** `.seed/05_Onotology_for_Nuggets.md` · rule: `.cursor/rules/proj-05-spiderfeet-nugget-ontology.mdc`
- **Widget Data Viewer embed:** `@spiderfeet-widget/.docs/data-viewer-embed.md` (Structured tabs, postMessage contract)

## Stage 4 — Tests corpus (read before seed or Tests work)

| Topic | Where |
|-------|--------|
| **Agent guide** | `.docs/analysis/stage4_seed_corpus_and_tests.md` |
| **Smoke seeds** | `.docs/analysis/module_test_seeds.json` |
| **Project rule** | `.cursor/rules/proj-04-spiderfeet-stage4-corpus.mdc` |
| **Pass semantics** | Positive: produced output · Negative: `module_execution.verdict = clean_miss` |
| **Hidden modules** | 8 upstream-broken services: `service_state: error` (excluded from Tests/Subscriptions) |
| **Probe scripts** | `.seed/scripts/validate_test_seeds.py`, `research_pending_seeds*.py`, `sync_service_state.py` |

None-tier seed research is **closed** (79 smoke + 8 error). Upstream-blocked modules need **module fixes**, not more seed tuning.

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
