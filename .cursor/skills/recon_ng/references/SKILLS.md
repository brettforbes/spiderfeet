# Recon-ng References Index

Execution-focused references for the Recon-ng skill (framework **5.1.2**, capture **2026-08-10**).

## Reference Files

| File | Topic |
|------|--------|
| `cli-options.md` | Captured launcher flags for `recon-ng`, `recon-cli`, `recon-web`; stealth / empty-module observation |
| `workspaces-and-database.md` | Workspace lifecycle, SQLite tables, `db query` validation |
| `marketplace-and-modules.md` | Marketplace install/search/info; disabled/stale modules |
| `module-io-paths-and-source.md` | `recon/<input>-<output>/` sequencing and SOURCE strategies |
| `keys-and-global-options.md` | API keys; captured global options (`NAMESERVER`, `PROXY`, …) |
| `automation-and-scripting.md` | Prefer `recon-cli`; resource scripts; script/spool |
| `reporting-and-recon-web.md` | `reporting/*`, recon-web UI and `/api/` |
| `nugget-mapping.md` | Workspace rows → SpiderFeet nuggets/edges |
| `development-api-and-metadata.md` | Module metadata, D/K markers, issue routing |
| `sources.md` | Canonical official and practitioner URLs |

## Operator docs

- `.docs/docs-for-cli-tools/recon-ng-Zero-to-Hero.md`
- `.docs/docs-for-cli-tools/recon-ng-CLI-Options.md` (full Captured help sections)

## Maintenance

- Launcher flags: only from `.tmp_reconng_help/` / live `--help` — never invent options.
- Official wiki/repo/marketplace define console behaviour; practitioner cheat sheets are tactics only.
- Prefer **`recon-cli`** for SpiderFeet automation after marketplace modules are installed.
- Update this index when adding references.
