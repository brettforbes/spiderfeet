# Metasploit → SpiderFeet Nugget Mapping

Derive graphs from **structured DB exports / table dumps** when available. Console text is operator-facing; use TextFSM only for fields that never appear in export.

Resolve colours/icons from `.docs/analysis/nuggets.json` + `nuggets_extension.json`. Instance ids via shared `graph_builder` (`nugget_id` + uuid5). IPs only through `core.ip_classify.classify_ip`.

## Field → nugget

| MSF source | Nugget id(s) | Notes |
|------------|--------------|-------|
| Host address (IPv4/IPv6) | `IP_ADDRESS` / `INTERNAL_IP_ADDRESS` / IPv6 ids via `classify_ip` | Never hardcode `IP_ADDRESS` for colon-form |
| Host name / DNS | `INTERNET_NAME` | Unresolved → `INTERNET_NAME_UNRESOLVED` when applicable |
| Open TCP port | `TCP_PORT_OPEN` | From `services` proto/port |
| Open UDP port | `UDP_PORT_OPEN` | When present |
| Service banner / info | `TCP_PORT_OPEN_BANNER` / related descriptors | Attach to port/host |
| OS fingerprint notes | `OPERATING_SYSTEM` | From notes/services info when authoritative |
| CVE vulnerability rows | `VULNERABILITY_CVE_CRITICAL` … `_LOW` or `VULNERABILITY_GENERAL` | Map severity when known; else general |
| Non-CVE vuln / module finding | `VULNERABILITY_GENERAL` | Keep module name in data/provenance |
| Creds / loot / session secrets | Controlled sensitive descriptors | Do not casually promote into public OSINT graphs |

## Suggested edges

| Edge | Typical endpoints |
|------|-------------------|
| `contains` | Scan/workspace → host |
| `has` | Host → port / name |
| `runs` | Host/port → service/OS descriptors |
| `affected_by` | Host/service → vulnerability |

Every node must appear in at least one edge. Deduplicate by `(nugget_id, nugget_data)`.

## Artifact roles (CLI profiling)

| Artifact | Role |
|----------|------|
| DB export XML/JSON or table dump | **Structured** source for graph |
| Derived host/service listing | **Text** pane (from structured) |
| `proposed_nuggets_edges.json` | Graph |
| Narrative MD | Markdown report |

Forbidden: shipping a text-only MSF scenario when a DB export was available for the same run.
