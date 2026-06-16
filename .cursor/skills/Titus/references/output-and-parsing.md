# Titus Output and Parsing

## Normalized schema

- `finding_id`
- `detector`
- `path`
- `confidence`
- `evidence_redacted`

## Parsing workflow

1. Export structured output when available.
2. Normalize each finding into parser schema.
3. Redact sensitive values.
4. De-duplicate by fingerprint and source root.
5. Assign confidence before nugget mapping.

## Example normalized record

```json
{
  "finding_id": "titus-001",
  "detector": "private-key",
  "path": "repo/config/key.pem",
  "confidence": "high",
  "evidence_redacted": true
}
```
