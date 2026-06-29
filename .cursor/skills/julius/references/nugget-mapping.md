# Julius → SpiderFeet Nugget Mapping

Parse **`julius probe -o jsonl`**. Derive graph from structured JSON, not table output.

## Primary mappings

| Julius field | Nugget type | Notes |
|--------------|-------------|-------|
| URL host | `INTERNET_NAME` or `IP_ADDRESS` | Parse `target` with `urlparse`; IPv4 literal → `IP_ADDRESS` |
| URL | `LINKED_URL_INTERNAL` | Full normalized base URL (scheme + host + port) |
| Open port (from URL) | `TCP_PORT_OPEN` | If not already present from Naabu/Nmap upstream |
| `service` | `SOFTWARE_USED` | `data` = probe name; `product` = humanized service |
| `category` | `DESCRIPTION_CATEGORY` | e.g. `self-hosted`, `gateway` |
| `specificity` | edge metadata / confidence | Store on `SOFTWARE_USED` source metadata |
| `matched_request` | `RAW_RIR_DATA` or metadata | Audit trail for fingerprint path |
| Each `models[]` entry | `SOFTWARE_USED` (child) | Model name under parent LLM service |
| `error` | `ERROR_MESSAGE` | When probe failed for target |

## Example nodes and edges

Input row:

```json
{
  "target": "https://10.0.0.5:11434/api/tags",
  "service": "ollama",
  "matched_request": "/api/tags",
  "category": "self-hosted",
  "specificity": 100,
  "models": ["llama3.2", "mistral"]
}
```

Suggested graph:

- `IP_ADDRESS` `10.0.0.5`
- `TCP_PORT_OPEN` `10.0.0.5:11434`
- `SOFTWARE_USED` `ollama` (category self-hosted, specificity 100)
- `SOFTWARE_USED` `llama3.2` ← child of ollama
- `SOFTWARE_USED` `mistral` ← child of ollama
- Edges: `IP_ADDRESS` → `TCP_PORT_OPEN` → `SOFTWARE_USED` (service) → model nodes

## Edge types

| From | To | Relationship |
|------|-----|--------------|
| Seed target | `IP_ADDRESS` / `INTERNET_NAME` | `RESOLVES_TO` / `AFFILIATE` |
| Host | `TCP_PORT_OPEN` | `OPEN_ON` |
| Port | `SOFTWARE_USED` (service) | `RUNS` |
| Service | Model `SOFTWARE_USED` | `PROVIDES_MODEL` |
| Service | `DESCRIPTION_CATEGORY` | `CATEGORIZED_AS` |

## Confidence policy

| `specificity` | Emit `SOFTWARE_USED`? |
|---------------|----------------------|
| ≥ 50 | Yes |
| 1 (`openai-compatible`) | Yes with `confidence: low` metadata |
| Row has `error` only | No service node; optional `ERROR_MESSAGE` |

## Augustus generator configs

When `--augustus` present and `generator_configs` populated, store as `RAW_RIR_DATA` or dedicated metadata blob for Augustus skill handoff — do not execute Augustus without authorization.

## Provenance

Every node should include:

- `source_tool`: `julius`
- `source_command`: full CLI with flags
- `source_artifact`: path to `.jsonl` file
- `matched_request`, `specificity`

## Deduplication

Key: `{host}:{port}:{service}`. For multiple specificity-sorted matches on same host, keep **highest specificity** unless operator requests full enumeration.
