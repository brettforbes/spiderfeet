# Module I/O Paths and SOURCE

## Path-first module selection

Recon-ng module paths encode dataflow intent as `recon/<input>-<output>/module_name`.
Use this path structure to decide sequence based on current workspace table state.

Common families:
- `recon/domains-hosts/*`
- `recon/hosts-ports/*`
- `recon/domains-contacts/*`
- `reporting/*` (export/output)

## Sequencing model

1. Identify current strongest table (for example `domains`).
2. Select modules whose `<input>` matches that table.
3. Execute and validate `<output>` table growth.
4. Promote newly grown table as next stage input.
5. Repeat until graph breadth plateaus.

## SOURCE option strategies

`SOURCE` controls seed inputs to module execution.

### 1) Literal/default SOURCE
- Use for initial sanity checks and small-scope runs.
- Best when you need immediate feedback on module viability.

### 2) File-backed SOURCE
- Use for curated bulk seeds gathered externally.
- Best for controlled batch execution and replayability.

### 3) SQL-backed SOURCE
- Use for adaptive in-workspace chaining.
- Best when dynamically selecting rows from existing tables (for example only unresolved hosts).

## SOURCE decision rules

- If first run and uncertain module quality -> use literal SOURCE.
- If large curated target list -> use file SOURCE.
- If chaining mature workspace outputs -> use SQL SOURCE.
- If quota is constrained -> use SQL SOURCE with filtered subsets.

## API spend and redundancy control

- Run modules against small representative seed slices before full runs.
- Track row deltas after each execution; stop modules with repeated zero-growth outcomes.
- Deduplicate or filter source rows before expensive providers.
- Prefer chaining from verified local tables over re-querying identical external data.

## Example path-driven pipeline

1. `domains` seed available.
2. Run `recon/domains-hosts/*` modules -> populate `hosts`.
3. Run `recon/domains-contacts/*` modules -> populate `contacts`.
4. Run `recon/hosts-ports/*` modules using `hosts` SOURCE -> populate `ports`.
5. Run `reporting/*` modules for export and downstream SpiderFeet ingest.
