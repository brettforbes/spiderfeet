# uncover JSONL → SpiderFeet Nugget Mapping

Derive nuggets from **`uncover -json`** JSON Lines, not from banner or `-f` text when JSONL exists.

**IP literals:** create address nodes only via `core.ip_classify.classify_ip` (IPv4 → `IPV4_ADDRESS` / related; IPv6 → `IPV6_ADDRESS`). Do not hardcode `IP_ADDRESS` for colon-form values.

## Primary mappings

| uncover field | nugget_id | Notes |
|---------------|-----------|-------|
| `ip` | classifier result | Via `classify_ip` |
| `host` (non-empty) | `INTERNET_NAME` | Hostname from provider; may be CDN/shared — validate |
| `port` (> 0) | `TCP_PORT_OPEN` | Provider-reported open port; value often `ip:port` or port string per graph convention |
| `url` (non-empty) | `URL` or link metadata | When present; many engines leave `url` empty |
| `source` | provenance meta | Engine id (`shodan`, `shodan-idb`, …) on edges / scan metadata |
| `timestamp` | scan / observation meta | Keep on structured record; optional TRACE narrative |

Uncover does **not** emit product/CVE fields in normalized JSONL — do not invent `WEBSERVER_TECHNOLOGY` / `VULNERABILITY_*` from JSON alone. Product clues live in the **query** (dork), not in the result object; enrich with httpx / nuclei / webanalyze after validation.

## Edges (practical)

Prefer shared ontology relations (`contains`, `had`, `listens-to`) when promoting to TypeDB. Examination graphs often use descriptive labels for review:

| Relationship | Shape |
|--------------|--------|
| name → address | `INTERNET_NAME` → IPv4/IPv6 (`resolves_to` / `had`) when both present |
| address → port | address → `TCP_PORT_OPEN` (`listens-to` / open-port) |
| scan → findings | scan head `contains` hosts/ports |

## Example: shodan-idb row

Input:

```json
{"timestamp":1786295459,"source":"shodan-idb","ip":"1.1.1.1","port":443,"host":"example.com","url":""}
```

Illustrative graph contract:

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "example.com"},
    {"type": "IPV4_ADDRESS", "data": "1.1.1.1"},
    {"type": "TCP_PORT_OPEN", "data": "1.1.1.1:443"}
  ],
  "edges": [
    {"source": "example.com", "target": "1.1.1.1", "relationship": "resolves_to"},
    {"source": "1.1.1.1", "target": "1.1.1.1:443", "relationship": "listens-to"}
  ]
}
```

Retain `source: shodan-idb` in structured metadata / edge props for confidence tracking.

## Sparse rows

| Shape | Mapping |
|-------|---------|
| `ip` + `port`, empty `host` | Address + `TCP_PORT_OPEN` only |
| `host` only (`ip` empty / `port` 0) | `INTERNET_NAME` only — common when `-f` falls back; rare in well-formed JSONL |
| Empty run | Scan head + empty/sparse tree (valid clean-miss graph) |

## Deduplication

- Node identity: `nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"` via shared `graph_builder`.
- Merge duplicate `(ip, port)` across engines; union `source` list on provenance.
- Cross-engine agreement increases confidence — still validate live before severity claims.

## Provenance (corpus / Tests tab)

- `source_tool`: `uncover`
- `source_command`: full CLI
- `source_artifact`: path to JSONL or harvest bundle
- `provider_engines`: values from `source` fields / `-e` list
- `query`: `-q` / per-engine query text (redact secrets)

## Downstream

| Tool | Input from uncover |
|------|--------------------|
| naabu | Unique `ip` (or `-f ip` pipe) for active port confirm |
| httpx | `ip:port`, host, or `-f https://ip:port` |
| nuclei | Live URLs after httpx |
| nerva | Confirmed open ports for fingerprint |
| dnsx | Hostnames needing resolve validation |

## Do not emit

- `TCP_PORT_OPEN` without IP (or resolvable host context)
- Vuln/tech nuggets inferred only from the search query string
- Orphan port nodes with no owning address/host
