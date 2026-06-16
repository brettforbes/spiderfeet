# NTLMRecon Output and Parsing

## Normalized schema

- `target`
- `hostname`
- `domain`
- `dns_domain`
- `signing_state`
- `confidence`

## Parsing workflow

1. Capture raw output per target.
2. Parse key fields into normalized records.
3. Standardize host/domain naming format.
4. Assign confidence to uncertain fields.

## Example normalized record

```json
{
  "target": "10.10.10.20",
  "hostname": "DC01",
  "domain": "CORP",
  "dns_domain": "corp.local",
  "signing_state": "required",
  "confidence": "medium"
}
```
