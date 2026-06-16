# dnsx Output Schema and Parsing

dnsx emits line-oriented results. Prefer JSON mode (`-j`) for robust automation.

## Parsing model

1. Read stdout line by line.
2. Skip empty/non-JSON lines.
3. Parse each JSON object defensively (field presence is option-dependent).
4. Normalize to internal shape:
   - `query_name`
   - `record_type`
   - `record_value`
   - `resolver`
   - `raw_answer`
5. Accumulate into deduplicated entity and relation sets.

## Practical field groups

| Group | Typical fields |
|---|---|
| Query identity | hostname/domain queried |
| Answer context | record type, value, TTL/class if available |
| Resolution metadata | resolver, status/error, timing where exposed |
| Raw payload | original response string/object |

## Example parser skeleton

```python
import json

for line in open("dnsx.jsonl", "r", encoding="utf-8"):
    line = line.strip()
    if not line or not line.startswith("{"):
        continue
    try:
        item = json.loads(line)
    except json.JSONDecodeError:
        continue

    # Normalize based on available keys in your dnsx version.
    # Store both normalized and raw values for traceability.
```

## Error and edge handling

- Handle NXDOMAIN, SERVFAIL, timeout, and empty-answer states separately.
- Do not infer "nonexistent host" from one failed resolver response.
- Support multi-value answers (multiple A/MX/NS records).
- Preserve original casing/punycode while normalizing host comparisons case-insensitively.
