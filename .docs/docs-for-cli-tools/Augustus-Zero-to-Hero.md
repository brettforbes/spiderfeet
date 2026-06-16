# Augustus Zero to Hero

Augustus is a production-focused LLM vulnerability scanner with probes, detectors, buffs, and multi-turn attack strategies.

## 1) Install

```bash
go install github.com/praetorian-inc/augustus/cmd/augustus@latest
```

## 2) Discover capabilities

```bash
augustus list
```

## 3) First scan

```bash
augustus scan openai.OpenAI \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --format jsonl \
  --output out.jsonl
```

## 4) Expand coverage

```bash
augustus scan openai.OpenAI \
  --probes-glob "dan.*,goodside.*" \
  --detectors-glob "*" \
  --config-file config.yaml \
  --output batch.jsonl
```

## 5) Test evasions with buffs

```bash
augustus scan anthropic.Anthropic \
  --probes-glob "dan.*" \
  --buffs-glob "encoding.*,paraphrase.*" \
  --format jsonl \
  --output buffed.jsonl
```

## 6) Multi-turn attacks

Use multi-turn probes (`crescendo`, `goat`, `hydra`, `mischievous`) with explicit `judge` config and larger timeouts.

## 7) Convert to SpiderFeet nuggets

Map each finding into graph arrays:
- nodes: model endpoint, probe, detector, vulnerability finding
- edges: tested_with, evaluated_by, identified

## 8) Common pitfalls

- missing judge config for judge-based/multi-turn probes
- over-parallelizing into provider rate limits
- losing run metadata needed for reproducibility
