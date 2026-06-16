# Augustus Output and Parsing

Augustus supports `table`, `json`, `jsonl`, and `html` outputs. For automation, prefer `jsonl`.

## Parsing priorities

1. Parse each attempt/finding record as one event.
2. Preserve generator, model config, probe, detector, score, and pass/fail status.
3. Keep timeout/error records; they indicate coverage gaps and runtime constraints.
4. Separate execution failures from model-safe outcomes.

## Suggested normalized record

```json
{
  "generator": "openai.OpenAI",
  "model": "gpt-4",
  "probe": "dan.Dan_11_0",
  "detector": "dan.DAN",
  "score": 0.85,
  "status": "VULN",
  "passed": false
}
```

## Parser guardrails

- Handle provider-specific response variance.
- Preserve run metadata (timeouts, concurrency, buffs, config file/profile).
- Avoid collapsing multi-turn attempts into single undifferentiated records.
