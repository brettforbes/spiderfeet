# NTLMRecon Zero-to-Hero

## Quick start

```bash
ntlmrecon -t 10.10.10.20
```

## End-to-end workflow

1. Probe approved hosts.
2. Parse challenge metadata.
3. Normalize and deduplicate records.
4. Convert validated data to nugget `nodes`/`edges`.
5. Escalate hardening findings.

## Strategies and tactics

- Probe domain controllers first.
- Expand to critical servers.
- Re-probe ambiguous hosts and compare.

## Nugget conversion example

```json
{
  "nodes": [{"id": "ip:10.10.10.20", "type": "IP_ADDRESS", "label": "10.10.10.20"}],
  "edges": []
}
```
