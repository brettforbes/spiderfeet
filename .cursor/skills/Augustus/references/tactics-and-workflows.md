# Augustus Tactics and Workflows

## Workflow A: Smoke test

1. One generator
2. One probe
3. One detector
4. JSONL output

Goal: validate auth/config/connectivity and parser behavior.

## Workflow B: Thematic batch

1. Use probe glob for one attack family (`dan.*`, `goodside.*`).
2. Use detector glob aligned with selected probes.
3. Tune concurrency/timeout.
4. Export JSONL + HTML.

## Workflow C: Evasion resilience

1. Baseline run without buffs.
2. Re-run with encoding/paraphrase/poetry buffs.
3. Compare vulnerability rate deltas.

## Workflow D: Multi-turn strategy testing

Use `crescendo`, `goat`, `hydra`, and `mischievous` probes with explicit judge configuration and longer timeouts.

## Tactics

- Start narrow, then expand.
- Keep deterministic config snapshots per run.
- Prioritize high-score repeated findings across independent probes.
