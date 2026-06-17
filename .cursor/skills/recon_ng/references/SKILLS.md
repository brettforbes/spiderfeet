# Recon-ng References Index

This directory breaks Recon-ng source material into execution-focused references for skill maintenance and operational usage.

## Reference Files

- `workspaces-and-database.md`
  - Workspace lifecycle, engagement isolation, SQLite usage patterns, and `db query` validation loops.

- `marketplace-and-modules.md`
  - Marketplace lifecycle, install/remove/update/search/info patterns, and module category navigation.

- `module-io-paths-and-source.md`
  - `recon/<input>-<output>/` path heuristics, module sequencing, and `SOURCE` strategies (literal/file/SQL).

- `keys-and-global-options.md`
  - API key management, provider dependencies, quota-safe operation, and global framework options.

- `automation-and-scripting.md`
  - `recon-ng -r`, `recon-cli`, script record/execute, and spool/log capture for repeatable runs.

- `reporting-and-recon-web.md`
  - Reporting modules, export usage, and recon-web context for review and downstream ingestion.

- `development-api-and-metadata.md`
  - Module metadata fields, dependency/key signals, framework API concepts, and marketplace indexing implications.

- `sources.md`
  - Canonical source URL inventory used by this skill and its docs.

## Maintenance Notes

- Treat official repository/wiki/marketplace sources as authoritative behavior definitions.
- Use practitioner references for workflow tactics only when they do not contradict official docs.
- Update this index when adding new references so SKILL consumers have one stable entrypoint.
