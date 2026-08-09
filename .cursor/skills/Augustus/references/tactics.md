# Augustus Tactics and Workflows

## Workflow A — Smoke test

1. Confirm auth/config (`OPENAI_API_KEY`, YAML, or `rest.Rest` URI).
2. Optional: `augustus scan test.Blank --probe dan.Dan_11_0 --detector dan.DAN --format json` to validate CLI/parser without remote spend.
3. One real generator + one `--probe` + one `--detector`.
4. Emit `--format json` and/or `-o smoke.jsonl`.
5. Confirm attempt records parse before any glob/`--all` run.

## Workflow B — Thematic batch

1. Pick an attack family via `--probes-glob` (e.g. `dan.*`, `goodside.*`, `grandma.*`).
2. Align `--detectors-glob` (or explicit `--detector` list).
3. Tune `--concurrency` / `--timeout`.
4. Export JSON/JSONL (+ optional `--html`).

## Workflow C — Evasion resilience (buffs)

1. Baseline thematic run **without** buffs.
2. Re-run with `-b` / `--buffs-glob` (e.g. `encoding.*`, paraphrase/poetry families from `augustus list`).
3. Diff vulnerability rate / scores between baseline and buffed JSONL.

## Workflow D — Multi-turn strategies

1. Complete single-turn baseline first.
2. Select probe (`crescendo.Crescendo`, `goat.Goat`, `hydra.Hydra`, `mischievous.MischievousUser` — verify names via `augustus list`).
3. Supply YAML with `judge` + attacker generator config (upstream README patterns).
4. Raise `--timeout`; keep concurrency modest.
5. Prefer `--format json` / `-o` + `--html` for review.

## Workflow E — Recon then probe

1. When MCP / agent tooling is in scope: `--recon recon.MCP` (also `recon.MCPConfig`, `recon.MCPIdentifiers` on this binary).
2. Help states recon may run with or without probes.
3. Follow with targeted `--probe` sets based on observations.

## Workflow F — Custom REST / Julius handoff

1. Fingerprint inference URLs with **Julius** (or httpx) on authorized hosts.
2. Configure `rest.Rest` (`uri`, templates, `response_json_field`).
3. Smoke one probe; then thematic batches.
4. Add `--refusal-pattern` if custom guardrail text causes false positives.

## Tactics

| Situation | Action |
|-----------|--------|
| Paid API, unknown spend | Smoke + small globs; never `--all` first |
| Rate limits | Lower `--concurrency`; extend `--timeout` / `--probe-timeout` |
| Custom guardrails | `--refusal-pattern` (repeatable) |
| Need stakeholder PDF-like view | `--html` alongside JSONL — HTML is not the graph source |
| Need corpus | Always structured JSON/JSONL; harvest to `records[]` bundle |
| Offensive probe families (`lmrc`, etc.) | Authorized labs only; warn operators |
| Hooked / dynamic targets | `--setup` / `--prepare` / `--cleanup` per Captured help |
| Harness choice | Default `probewise.Probewise`; `batch.Batch` / `agentwise.Agentwise` when listed and required |

## Pipeline sketches

```bash
# Fingerprint → adversarial test
# (Julius separately) then:
augustus scan rest.Rest --config-file target.yaml \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --format json -o dan.jsonl

# Baseline vs buffed
augustus scan openai.OpenAI --probes-glob "dan.*" --detectors-glob "*" -o base.jsonl --format json
augustus scan openai.OpenAI --probes-glob "dan.*" --detectors-glob "*" \
  --buffs-glob "encoding.*" -o buffed.jsonl --format json
```

## Expansion checklist

1. Auth / config works on smoke?
2. Structured JSON/JSONL parsing green?
3. Detectors aligned to probe family?
4. Refusal patterns tuned for this product?
5. Buffs / multi-turn only after baseline?
6. Secrets redacted before sharing artifacts?
