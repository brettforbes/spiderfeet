# tldfinder Strategies, Tactics, and Workflows

## Strategy: discover, score, validate, pivot

Use tldfinder as an upstream namespace discovery stage, then validate candidate namespaces before active scanning.

## Workflow 1 - Seed-driven discovery

1. Gather seeds from known domains, cert SANs, and passive DNS.
2. Run tldfinder in structured output mode.
3. Rank candidates by confidence/evidence volume.

## Workflow 2 - Namespace validation

1. Select top candidate suffixes.
2. Expand plausible host patterns under each candidate.
3. Resolve expanded hosts with dnsx across trusted resolvers.

## Workflow 3 - Split-horizon detection

1. Re-run from alternate resolver sets/vantage points.
2. Compare candidate suffix recurrence and host resolution behavior.
3. Flag likely split-horizon/private namespace artifacts.

## Workflow 4 - Graph-first pivoting

1. Convert validated findings to `nodes[]`/`edges[]`.
2. Push host candidates into HTTP and service fingerprint queues.
3. Feed confirmed infrastructure back into iterative discovery loops.

## Adaptive matrix

| Observation | Action |
|---|---|
| Low-confidence noise | tighten thresholds and require multi-seed recurrence |
| High-confidence private suffix | expand host candidates and resolve actively |
| Conflicting public/private interpretation | check PSL/root references and reclassify |
| Sparse results | broaden seed collection from related org assets |
