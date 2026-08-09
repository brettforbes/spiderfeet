# Recon-ng → SpiderFeet Nugget Mapping

Map **structured workspace rows** (SQL extracts or `reporting/*` machine-readable exports) into SpiderFeet nugget graphs. Do not treat interactive TUI banners as the graph source when structured exports exist.

Align with `.seed/04_Driving and Integrating_CLI_Apps.md`, `.seed/05_Onotology_for_Nuggets.md`, and catalogue files `.docs/analysis/nuggets.json` + `nuggets_extension.json`. Reuse existing `nugget_id` values before inventing types.

## Table → nugget

| Workspace / export field | Preferred nugget_id | Notes |
|--------------------------|---------------------|--------|
| Domain name | `DOMAIN_NAME` or `INTERNET_NAME` | Prefer catalogue match for the value class |
| Hostname / FQDN | `INTERNET_NAME` | |
| IPv4 / IPv6 literal | via `core.ip_classify.classify_ip` | Never hardcode ambiguous `IP_ADDRESS` |
| Contact name | `HUMAN_NAME` | |
| Email | `EMAILADDR` | |
| Phone | `PHONE_NUMBER` | |
| Open TCP/UDP port | `TCP_PORT_OPEN` / `UDP_PORT_OPEN` | |
| Vulnerability / CVE text | `VULNERABILITY_GENERAL` (+ CVE tier types when present) | |
| Module/provider blob with no better fit | `RAW_RIR_DATA` (last resort) | Document unmapped fields in structure docs |

## Edges

| Relation | Use |
|----------|-----|
| `contains` | Domain contains host; host contains port; org/system containment |
| `had` | Entity had descriptor (email, phone, vendor string, etc.) |

Do not invent Nexus or ad-hoc relation names without seed/spec update.

## Identity

Use shared `graph_builder` identity:

```text
nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"
```

One node per `(nugget_id, nugget_data)`; reuse nodes and link with edges.

## Pipeline outputs

| Tab | Source |
|-----|--------|
| Text | Spool / reporting narrative (human review) |
| Structured / Data | SQL query results or reporting CSV/JSON/XML |
| Graph | Nodes/edges derived from structured rows only |

Empty clean-miss tables still produce a valid sparse graph (scan head + empty host tree) once formal examination is wired — do not ship scenarios without graphs.
