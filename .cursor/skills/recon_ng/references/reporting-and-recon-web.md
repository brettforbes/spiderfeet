# Reporting and Recon-web

## Reporting modules

The `reporting/*` module family converts workspace data into exportable outputs for review, handoff, and downstream ingestion.

Use cases:
- Human-readable summaries for analysts/operators.
- Structured exports for pipeline ingestion.
- Evidence bundles for engagement records.

## Reporting workflow

1. Validate workspace tables (`domains`, `hosts`, `contacts`, `ports`, vulnerabilities-related rows).
2. Load relevant `reporting/*` module.
3. Configure output options and destination paths.
4. Execute and verify artifact integrity.
5. Ingest outputs into SpiderFeet text/data/graph processing paths.

## recon-web role

Recon-web provides a web interface context for reviewing workspaces and results. It is useful for collaborative review and visual inspection when console-only interaction is insufficient.

Operational caution:
- Treat recon-web as a presentation/review layer, not a substitute for direct table validation with `db query`.

## Export strategy for SpiderFeet

Export priorities:
1. Preserve raw report text for audit/context (text tab).
2. Preserve normalized record sets for table-based display (data tab).
3. Preserve relationship-capable data for graph node/edge synthesis (graph tab).

## Common pitfalls

- Exporting before validating table completeness.
- Assuming report success equals complete dataset quality.
- Losing workspace identifier context in exported file names.

Use deterministic naming:
- `<workspace>-<module-family>-<timestamp>.<ext>`
