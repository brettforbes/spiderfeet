# Katana Tactics and Workflows

## Workflow: Baseline then Deepen

1. Start shallow crawl (`depth 2-3`).
2. Parse and cluster routes by host/path family.
3. Deepen only high-signal targets.

## Workflow: JS-heavy Apps

1. Re-run with `-jc`.
2. Extract API paths and auth routes.
3. Feed results to follow-up scanners.

## Workflow: Sensitive Artifact Sweep

1. Run with `-kf` and optional form extraction.
2. Prioritize admin, backup, config, and upload paths.

## Tactics

- Broad-to-narrow sequencing.
- Constrain scope early.
- Deduplicate aggressively.
- Record provenance for every discovered URL.
