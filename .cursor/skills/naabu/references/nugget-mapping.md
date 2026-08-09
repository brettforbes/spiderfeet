# Naabu JSONL → SpiderFeet Nugget Mapping

Convert **`-json`** JSON Lines into graph payloads with `nodes[]` and `edges[]`. Catalogue ids from `.docs/analysis/nuggets.json` / `nuggets_extension.json`.

**IP literals:** create address nodes only via `core.ip_classify.classify_ip` (IPv4 → `IPV4_ADDRESS` / related; IPv6 → `IPV6_ADDRESS`). Do not hardcode `IP_ADDRESS` for colon-form values. (Legacy notes may say `IP_ADDRESS`; prefer classifier output.)

## Primary mappings

| naabu field / signal | nugget_id | `data` / notes |
|----------------------|-----------|----------------|
| `host` | `INTERNET_NAME` | FQDN when present |
| `ip` | classifier result | Via `classify_ip` |
| `port` + TCP (`protocol` tcp / default) | `TCP_PORT_OPEN` | Prefer `ip:port` or host-qualified form used by adapter |
| `port` + UDP (`protocol` udp or `u:` input) | `UDP_PORT_OPEN` | When UDP was requested |
| `-cdn` / CDN label | `PROVIDER_HOSTING` (or meta) | When CDN name present |
| service/version from `-sD`/`-sV` | `SOFTWARE_USED` / related | Only when fields appear in JSONL sample |
| `tls: true` | metadata on port | Do not invent a nugget type unless catalogue supports it |

## Edges (practical)

Prefer shared ontology relations (`contains`, `had`, `listens-to`) when promoting to TypeDB; examination graphs often use descriptive labels for operator review:

| Relationship | Shape |
|--------------|--------|
| host → IPv4/IPv6 | `INTERNET_NAME` → address (`resolves_to` / `had`) |
| address → open TCP port | address → `TCP_PORT_OPEN` (`listens-to` / `had`) |
| address → open UDP port | address → `UDP_PORT_OPEN` (`listens-to` / `had`) |
| port → software | port → `SOFTWARE_USED` (`had`) when `-sV`/`-sD` enrich |

## Example: CONNECT JSONL rows

Input:

```json
{"host":"scanme.nmap.org","ip":"45.33.32.156","timestamp":"2026-08-10T00:00:00Z","port":80,"protocol":"tcp","tls":false}
{"host":"scanme.nmap.org","ip":"45.33.32.156","timestamp":"2026-08-10T00:00:00Z","port":22,"protocol":"tcp","tls":false}
```

Output contract (illustrative):

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "scanme.nmap.org"},
    {"type": "IPV4_ADDRESS", "data": "45.33.32.156"},
    {"type": "TCP_PORT_OPEN", "data": "45.33.32.156:80"},
    {"type": "TCP_PORT_OPEN", "data": "45.33.32.156:22"}
  ],
  "edges": [
    {"source": "scanme.nmap.org", "target": "45.33.32.156", "relationship": "resolves_to"},
    {"source": "45.33.32.156", "target": "45.33.32.156:80", "relationship": "listens-to"},
    {"source": "45.33.32.156", "target": "45.33.32.156:22", "relationship": "listens-to"}
  ]
}
```

IPv6 rows from the same hostname get `IPV6_ADDRESS` nodes via `classify_ip`.

## Passive scan provenance

Records from `-passive` (InternetDB) should record:

- `source_tool`: `naabu`
- `scan_type` / mode: `passive`
- Do not treat as active confirmation without optional active re-scan

## Deduplication

Key: `{ip}:{port}:{protocol}` — merge duplicate lines from `-sa` multi-IP hostname scans and dual-stack retries.

## Downstream edges

| Next tool | Edge intent |
|-----------|-------------|
| Nerva | Port → service fingerprint |
| httpx | Port 80/443/8080/… → web content |
| Julius | AI ports → LLM service |
| Nmap NSE | Port → vulnerability script results |

## Provenance fields

Every nugget should record:

- `source_tool`: `naabu`
- `source_command`: full CLI (include `-json`)
- `source_artifact`: path to `.jsonl` / structured bundle
- `scan_type`: `syn`, `connect`, or `passive`

## Do not emit

- Closed or filtered ports (naabu only reports open/reply ports)
- `TCP_PORT_OPEN` without IP or resolvable host context
- Ambiguous `IP_ADDRESS` for IPv6 literals
