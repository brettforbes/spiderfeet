# Naabu JSONL → SpiderFeet Nugget Mapping

Derive nuggets from **`naabu -json`** JSON Lines, not from banner text.

## Primary mappings

| JSON field | Nugget type | Notes |
|------------|-------------|-------|
| `ip` | `IP_ADDRESS` | Canonical when present |
| `host` | `INTERNET_NAME` | When hostname scanned |
| `port` + TCP | `TCP_PORT_OPEN` | Default for most scans |
| `port` + UDP (`u:` input) | `UDP_PORT_OPEN` | When protocol is udp |
| `service` | `SOFTWARE_USED` | With `-sD` / `-sV` |
| `version` | `SOFTWARE_USED` | Product/version from `-sV` |
| `tls` | metadata on port | TLS-enabled port flag |
| `cdn` | `PROVIDER_HOSTING` or metadata | CDN attribution |

## Example nodes and edges

Input:

```json
{"host":"scanme.sh","ip":"45.33.32.156","port":22}
{"host":"scanme.sh","ip":"45.33.32.156","port":80}
```

Graph:

- `INTERNET_NAME` scanme.sh
- `IP_ADDRESS` 45.33.32.156
- `TCP_PORT_OPEN` 45.33.32.156:22
- `TCP_PORT_OPEN` 45.33.32.156:80
- Edges: `INTERNET_NAME` → `RESOLVES_TO` → `IP_ADDRESS`; `IP_ADDRESS` → `OPEN` → each port

## With service version

```json
{"host":"scanme.sh","ip":"45.33.32.156","port":22,"service":"ssh","version":"OpenSSH 6.6.1p1"}
```

Add `SOFTWARE_USED` linked to port: product OpenSSH, version 6.6.1p1.

## Passive scan provenance

Records from `-passive` (InternetDB) should include metadata:

- `source`: `naabu_passive`
- Do not treat as active scan confirmation without optional active re-scan

## Deduplication key

`{ip}:{port}:{protocol}` — merge duplicate lines from `-sa` multi-IP hostname scans.

## Downstream edges

| Next tool | Edge intent |
|-----------|-------------|
| Nerva | Port → service fingerprint |
| httpx | Port 80/443/8080 → web content |
| Julius | AI ports → LLM service |
| Nmap NSE | Port → vulnerability script results |

## Provenance fields

Every nugget should record:

- `source_tool`: `naabu`
- `source_command`: full CLI
- `source_artifact`: path to `.jsonl`
- `scan_type`: `syn`, `connect`, or `passive`

## Do not emit

- Closed or filtered ports (naabu only reports open/reply ports)
- `TCP_PORT_OPEN` without IP or resolvable host context

## Legacy module note

SpiderFeet may integrate naabu via `sfp_tool_*` wrappers — same nugget types as Nmap port events where overlap exists; prefer naabu JSON for new corpus work.
