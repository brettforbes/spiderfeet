# Nosey-Parker Zero-to-Hero

## Quick start

```bash
noseyparker scan --datastore ./np-ds ./repo
noseyparker report --datastore ./np-ds
```

## End-to-end workflow

1. Baseline scan.
2. Triage high-confidence results.
3. Validate context and deduplicate.
4. Export structured output.
5. Convert validated findings to nugget `nodes`/`edges`.
6. Remediate and re-scan.

## Strategies and tactics

- Broad pass first, then focused pass.
- Prioritize cloud keys/tokens/private keys.
- Track deltas across repeated scans.

## Nugget conversion example

```json
{
  "nodes": [{"id": "finding:np:1", "type": "RAW_RIR_DATA", "label": "possible secret"}],
  "edges": []
}
```
