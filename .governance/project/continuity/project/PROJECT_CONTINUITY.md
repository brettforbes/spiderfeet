# Project Continuity

Durable context for the spiderfeet fork.

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

## Next durable actions

See `.governance/project/BACKLOG.md` and `INIT-TODO.md`.
