# Titus Zero-to-Hero

## Quick start

```bash
titus scan ./repo
```

## End-to-end workflow

1. Baseline scan.
2. Triage by confidence and detector type.
3. Validate context and deduplicate.
4. Export structured output.
5. Convert validated findings to nugget `nodes`/`edges`.
6. Remediate and verify with re-scan.

## Strategies and tactics

- Run phased scans for large repositories.
- Prioritize high-impact secret classes first.
- Track finding deltas over time.

## Nugget conversion example

```json
{
  "nodes": [{"id": "finding:titus:1", "type": "RAW_RIR_DATA", "label": "possible secret"}],
  "edges": []
}
```
