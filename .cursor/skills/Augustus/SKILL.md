---
name: Augustus
description: Run LLM vulnerability scans with Augustus for prompt injection, jailbreak, extraction, and adversarial safety testing. Trigger when evaluating model safety posture, scanning prompts at scale, validating guardrails, or generating JSON/JSONL evidence for security reports.
---

# Augustus - LLM Vulnerability Scanner

## Purpose

Use this skill when you need structured offensive testing of LLM systems using probes, detectors, buffs, and repeatable evidence outputs, with conversion to SpiderFeet-style nugget node/edge arrays.

## Step-by-Step Instructions

1. Confirm authorization for testing target model/provider.
2. Select generator (provider), probe scope, and detectors.
3. Start with a small probe set (single probe or narrow glob).
4. Run scan with JSON/JSONL output for machine parsing.
5. Expand to broader probe suites (`--all` or glob classes) only after baseline validation.
6. Apply buffs when evaluating evasion resistance (encoding/paraphrase/poetry/etc.).
7. Normalize results and convert to SpiderFeet-style nuggets:
   - `nodes`: model endpoint, probe family, detector, finding.
   - `edges`: probe tested model, detector marked finding, finding belongs-to category.

## If/Then Decision Rules

- If target is OpenAI/Anthropic/etc., then use provider generator directly.
- If target is custom endpoint, then use `rest.Rest` with request/response mapping.
- If judge-based probes or multi-turn probes are used, then include required `judge` config.
- If rate limits trigger failures, then lower concurrency and extend timeout.
- If result needs automation, then use `--format jsonl` and output file.
- If quick smoke test is needed, then run one probe + one detector before broad runs.

## Guardrails & Pitfalls

- Authorized testing only; outputs may include harmful/offensive content by design.
- Do not treat one failed probe as complete model compromise without context.
- Keep API keys and sensitive prompt/response data redacted in shared artifacts.
- Align detector choice with probe families to avoid misleading pass/fail interpretation.
- Track configuration (model, temperature, timeout, probe set) with each report.

## Strategies and Tactics

- Baseline -> broaden -> targeted retest workflow.
- Run both direct and buffed probes to evaluate evasion resilience.
- Use multi-turn strategies (Crescendo/GOAT/Hydra/Mischievous) for deeper guardrail evaluation.
- Prefer JSONL for SOC/reporting pipelines and historical trend analysis.

## References

See `references/SKILLS.md` for CLI options, output schema, nugget mapping, tactics/workflows, and sources.

## Examples

```bash
# Single probe smoke test
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN --format jsonl -o out.jsonl

# Batch by glob with buffs
augustus scan anthropic.Anthropic --probes-glob "dan.*,goodside.*" --buffs-glob "encoding.*" --format jsonl -o batch.jsonl

# Full scan on custom REST endpoint
augustus scan rest.Rest --all --config-file config.yaml --timeout 60m --html report.html

# Capability listing
augustus list
```
