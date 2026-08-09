# Julius → SpiderFeet Nugget Mapping

Parse **`julius probe -o json`** / **`-o jsonl`**. Derive graph from structured JSON, not table output.

## Primary mappings

| Julius field | Nugget type | Notes |
|--------------|-------------|-------|
| URL host (name) | `INTERNET_NAME` | DNS hostname from `target` |
| URL host (IPv4/IPv6) | via `classify_ip` | Never hardcode ambiguous `IP_ADDRESS`; use `IPV4_ADDRESS` / `IPV6_ADDRESS` / internal variants |
| URL | `LINKED_URL_INTERNAL` | Scheme + host + port (base URL) |
| Open port (from URL) | `TCP_PORT_OPEN` | If not already present from Naabu/Nmap |
| `service` | `SOFTWARE_USED` | Probe name; keep specificity/category in metadata |
| `category` | `DESCRIPTION_CATEGORY` or metadata | e.g. `self-hosted`, `gateway`, `mcp` |
| `specificity` | metadata / confidence | On `SOFTWARE_USED` |
| `matched_request` | metadata or `RAW_RIR_DATA` | Fingerprint path audit |
| Each `models[]` entry | `SOFTWARE_USED` (child) | Model name under parent LLM service |
| `error` | `ERROR_MESSAGE` | When probe failed for target |

Reuse catalogue ids from `.docs/analysis/nuggets.json` / `nuggets_extension.json` before inventing types.

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

- Address node for `10.0.0.5` (via `classify_ip`)
- `TCP_PORT_OPEN` `10.0.0.5:11434`
- `SOFTWARE_USED` `ollama` (category self-hosted, specificity 100)
- `SOFTWARE_USED` `llama3.2` / `mistral` as children
- Edges: host → port → service → models (`contains` / `had` per ontology pack)

## Confidence policy

| `specificity` | Emit `SOFTWARE_USED`? |
|---------------|----------------------|
| ≥ 50 | Yes |
| 1 (`openai-compatible`) | Yes with `confidence: low` metadata |
| Row has `error` only | No service node; optional `ERROR_MESSAGE` |

## Augustus generator configs

When `--augustus` is set and `generator_configs` is populated, store as metadata / `RAW_RIR_DATA` for Augustus handoff — do not execute Augustus without authorization.

## Provenance

Every node should include:

- `source_tool`: `julius`
- `source_command`: full CLI with flags
- `source_artifact`: path to structured capture
- `matched_request`, `specificity`

## Deduplication

Key: `{host}:{port}:{service}`. Keep **highest specificity** unless operator requests full enumeration.
