# Project Continuity

Durable context for the spiderFeet fork.

## Module taxonomy (2026-05-23)

| Class | Count | Reference |
|-------|------:|-----------|
| OSINT services (`dataSource` in meta) | 177 | `.docs/analysis/osint_services.json` |
| Quarantined (specialised, unverified) | 54 | `.docs/quarantine_modules.md` |
| Core non-OSINT (generic infrastructure) | 2 | `.docs/non_osint_modules.md` |

Only `sfp__stor_db` and `sfp__stor_stdout` are confirmed generic non-OSINT modules.

## Governance

- VibeGov bootstrap **init** completed 2026-05-23 (scaffold only; GitHub board blocked).
- Active spec: `SPEC-001-governance-bootstrap.md`
- Product intent: **provisional** — analysis/documentation phase

## Conventions

- Analysis scripts live under `.docs/analysis/`
- Regenerate module docs via `generate_non_osint_doc.py` / `analyse_modules.py`
- Agent commits forbidden unless operator requests

## Stage 4 seed corpus (2026-06-08)

- None-tier pool (87): **79 smoke-validated**, **8** `service_state: error` (upstream-blocked), research **100% closed**.
- Fixture semantics: positive = produced; negative = `module_execution.verdict = clean_miss`.
- `scan_ui` resolves catalogue nugget types via `scan_targets.py`.
- Tests/Subscriptions hide `error` modules; Maps still includes all.
- **Unmerged:** seed research + `service_state` work is local on `develop` until PR.
- **Agent doc:** `.docs/analysis/stage4_seed_corpus_and_tests.md`
- **Epic:** GitHub #674

## Next durable actions

1. PR local `develop` changes (seeds, scan_targets, service_state, module_execution).
2. Open module-fix issues for 8 upstream-blocked modules.
3. Maps UI: optional filter for `service_state: error`.
4. See `.governance/project/BACKLOG.md` and `INIT-TODO.md`.
