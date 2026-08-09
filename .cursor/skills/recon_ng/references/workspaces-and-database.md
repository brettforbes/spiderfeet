# Workspaces and Database

## Why workspaces exist

Workspaces isolate engagement data so module chaining, provenance, and reporting stay scoped to one authorization boundary. Cross-engagement contamination breaks SpiderFeet graph trust and API-spend accounting.

## Lifecycle

Interactive console (not launcher flags):

```text
workspaces create <name>
workspaces select <name>
workspaces list
```

Launcher shortcut (captured):

```text
recon-ng -w <workspace>
recon-cli -w <workspace> …
```

Naming: `<org>-<scope>-<date>` (example: `acme-ext-2026q3`).

## SQLite role

Each workspace persists module outputs in tables that become seeds for subsequent modules. That persistence is the advantage over one-shot CLIs.

Pattern:

1. Run module A (e.g. domains → hosts).
2. Validate inserts with `db query` / `show`.
3. Feed module B via table-derived `SOURCE` (prefer SQL for adaptive filters).
4. Stop when row growth plateaus.

## Quality gates

Between modules, require:

- Non-zero prerequisite table rows
- Distinct-value / freshness checks before expensive providers
- Explicit workspace selection before every automation batch

## Hygiene

- One workspace per authorization boundary
- Do not mix sandbox tests with production recon
- Snapshot/export before destructive cleanup
- Tie spool/script logs to workspace name

## SpiderFeet

Validated workspace rows (or reporting exports) are the structured source for text/data/graph tabs — not raw console chatter alone.
