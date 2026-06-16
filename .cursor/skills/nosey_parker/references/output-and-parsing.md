# nosey_parker Output and Parsing

## Normalized schema

- `finding_id`
- `rule`
- `source_path`
- `classification`
- `evidence_redacted`

## Parsing workflow

1. Prefer structured output export.
2. Redact raw secret values.
3. De-duplicate by rule + fingerprint + source root.
4. Assign confidence before graph promotion.

## Example normalized record

```json
{
  "finding_id": "np-001",
  "rule": "aws-access-key",
  "source_path": "repo/app/config.py",
  "classification": "high_confidence_secret",
  "evidence_redacted": true
}
```
