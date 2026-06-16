# Workspaces and Database

## Why workspaces exist

Recon-ng workspaces isolate engagement data so module chaining, row provenance, and reporting remain scoped to a single target/client context. This supports repeatability and prevents cross-engagement contamination.

## Workspace lifecycle

- Create: `workspaces create <name>`
- Select: `workspaces select <name>`
- List: `workspaces list`
- Remove/archive when engagement is complete (after exports and evidence capture).

Recommended naming:
- `<org>-<scope>-<date>` for deterministic sorting and handoff.

## SQLite role in workflow

Each workspace persists module output in tables that become the seed source for subsequent modules. This is the core advantage over one-shot CLI tools.

Operational pattern:
1. Run module A (for example domains -> hosts).
2. Validate inserted rows.
3. Feed module B using table-derived `SOURCE`.
4. Repeat until no meaningful row growth remains.

## Database inspection and quality checks

Use `db query` throughout execution to:
- confirm expected table growth,
- validate row quality before expensive API calls,
- detect duplicated/low-value data early,
- drive adaptive module selection.

Quality gates between modules:
- Non-zero prerequisite table rows.
- Distinct value count threshold (avoid rerunning on duplicates).
- Freshness checks when running long engagements.

## Workspace hygiene tactics

- One workspace per authorization boundary.
- Do not mix sandbox tests with production reconnaissance.
- Snapshot or export before destructive workspace changes.
- Keep an execution log (spool/script record) tied to workspace name.

## SpiderFeet integration implications

Workspace tables are the authoritative intermediate representation for:
- text evidence capture (console/reporting artifacts),
- tabular data output (normalized extracts),
- graph output (nugget nodes/edges).

For deterministic SpiderFeet ingestion, always extract from validated workspace rows rather than raw terminal text.
