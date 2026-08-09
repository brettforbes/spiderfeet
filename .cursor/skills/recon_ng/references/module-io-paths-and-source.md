# Module I/O Paths and SOURCE

## Path-first selection

Module paths encode dataflow: `recon/<input>-<output>/module_name`. Choose modules whose `<input>` matches a non-empty workspace table.

Common families:

- `recon/domains-hosts/*`
- `recon/hosts-ports/*`
- `recon/domains-contacts/*`
- `reporting/*`

## Sequencing

1. Identify strongest current table (e.g. `domains`).
2. Load modules whose `<input>` matches.
3. Run; validate `<output>` growth with `db query`.
4. Promote the grown table as the next stage input.
5. Stop when graph breadth / row growth plateaus.

## SOURCE strategies

`SOURCE` is the usual module seed option (set via console `options set` or `recon-cli -o SOURCE=…`).

| Mode | When |
|------|------|
| Literal / default | Smoke-test viability; tiny authorized seeds |
| File-backed | Curated bulk lists; replayable batches |
| SQL-backed | Adaptive chaining from workspace tables (e.g. only new hosts) |

### Decision rules

- Uncertain module → literal SOURCE first
- Large curated list → file SOURCE
- Mature workspace chaining → SQL SOURCE
- Quota constrained → SQL SOURCE with filters

## Spend and redundancy

- Sample slices before full provider runs
- Track row deltas; stop repeated zero-growth modules
- Deduplicate SOURCE before expensive APIs
- Prefer local table reuse over re-querying identical external data

## Example pipeline

1. Seed `domains`
2. `recon/domains-hosts/*` → `hosts`
3. `recon/domains-contacts/*` → `contacts` (parallel lane)
4. `recon/hosts-ports/*` with SQL SOURCE from `hosts` → `ports`
5. `reporting/*` for export / SpiderFeet ingest
