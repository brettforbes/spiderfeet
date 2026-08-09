# Nerva scan narrative — `tcp_http_rich_json`

## Introduction

The scan used Nerva. Findings are organised under each meta-concept present in the graph (ENVIRONMENT, NETWORKS, APPLICATIONS, VULNERABILITIES, SECURITY). This report follows Scan → Host/System → Trace → Appendix. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nerva:scanme.nmap.org:80:2026-06-30T07:38:43.148728+00:00`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`, `SCAN_TOOL`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_target_3["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_3
  scan_start_4["SCAN_START"]
  scan_record_1 -->|had| scan_start_4
  scan_elapsed_5["SCAN_ELAPSED"]
  scan_record_1 -->|had| scan_elapsed_5
  scan_exit_status_6["SCAN_EXIT_STATUS"]
  scan_record_1 -->|had| scan_exit_status_6
  scan_tool_7["SCAN_TOOL"]
  scan_record_1 -->|had| scan_tool_7
```

### `SCAN_CLI`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI: nerva -t scanme.nmap.org:80 --json -w 5…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nerva -t scanme.nmap.org:80 --json -w 5000` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: scanme.nmap.org:80"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `scanme.nmap.org:80` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-06-30T07:38:43.148728+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-06-30T07:38:43.148728+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 16.094"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `16.094` |

### `SCAN_EXIT_STATUS`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_exit_status_2["SCAN_EXIT_STATUS: 0"]
  scan_record_1 -->|contains| scan_exit_status_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_EXIT_STATUS` | `0` |

### `SCAN_TOOL`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_tool_2["SCAN_TOOL: nerva"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `nerva` |

## CDN

CDN edge endpoints replace HOST when fronting is detected; origin host count may be indeterminate. This scan includes **1** CDN root node(s) (e.g. `scanme.nmap.org`). Linked structures: `NETWORKS`, `APPLICATIONS`.

### Structure overview

```mermaid
flowchart TD
  cdn_1["CDN"]
  networks_2["NETWORKS"]
  cdn_1 -->|contains| networks_2
  applications_3["APPLICATIONS"]
  cdn_1 -->|contains| applications_3
```

### `NETWORKS`

```mermaid
flowchart TD
  networks_1["NETWORKS"]
  ipv4_address_2["IPV4_ADDRESS: 45.33.32.156"]
  networks_1 -->|contains| ipv4_address_2
  ipv6_address_3["IPV6_ADDRESS: 2600:3c01::f03c:91ff:fe18:bb2f"]
  networks_1 -->|contains| ipv6_address_3
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `45.33.32.156` |
| `IPV6_ADDRESS` | `2600:3c01::f03c:91ff:fe18:bb2f` |

### `APPLICATIONS`

```mermaid
flowchart TD
  applications_1["APPLICATIONS"]
  service_2["SERVICE: http"]
  applications_1 -->|contains| service_2
```

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http` |

## Services and ports

APPLICATION services listen-to PORT entities under NETWORKS/TRANSPORT. This scan includes **1** Services and ports root node(s) (e.g. `http`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  service_1["SERVICE"]
```

### Values

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:scanme.nmap.org` |
| `CDN` | `scanme.nmap.org` |
| `CDN_VENDOR` | `Netlify` |
| `CLASSIFICATION_RULE_FIRED` | `C1: Server/header signature (Netlify)` |
| `CPE_URL` | `cpe:2.3:a:apache:http_server:*:*:*:*:*:*:*:*` |
| `CPE_URL` | `cpe:2.3:a:apache:http_server:2.4.7:*:*:*:*:*:*:*` |
| `CPE_URL` | `cpe:2.3:o:canonical:ubuntu_linux:*:*:*:*:*:*:*:*` |
| `HOST_CLASSIFICATION` | `fronted_unknown` |
| `HTTP_STATUS_CODE` | `200` |
| `IPV4_ADDRESS` | `45.33.32.156` |
| `IPV6_ADDRESS` | `2600:3c01::f03c:91ff:fe18:bb2f` |
| `NETWORKS` | `networks:scanme.nmap.org` |
| `ORIGIN_FINGERPRINT_SUPPRESSED` | `True` |
| `ORIGIN_HOST_COUNT` | `indeterminate` |
| `PORT` | `80` |
| `SCAN_CLI` | `nerva -t scanme.nmap.org:80 --json -w 5000` |
| `SCAN_ELAPSED` | `16.094` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_RECORD` | `nerva:scanme.nmap.org:80:2026-06-30T07:38:43.148728+00:00` |
| `SCAN_START` | `2026-06-30T07:38:43.148728+00:00` |
| `SCAN_TARGET` | `scanme.nmap.org:80` |
| `SCAN_TOOL` | `nerva` |
| `SERVICE` | `http` |
| `SERVICE_VERSION` | `Apache/2.4.7 (Ubuntu)` |
| `SOFTWARE_USED` | `Apache HTTP Server:2.4.7` |
| `SOFTWARE_USED` | `Ubuntu` |
| `SOFTWARE_USED` | `apache_httpd:2.4.7` |
| `TLS_ENABLED` | `False` |
| `TRANSPORT` | `tcp` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `CDN` |
| `CDN` | `had` | `HOST_CLASSIFICATION` |
| `CDN` | `had` | `CLASSIFICATION_RULE_FIRED` |
| `CDN` | `had` | `CDN_VENDOR` |
| `CDN` | `had` | `ORIGIN_HOST_COUNT` |
| `CDN` | `contains` | `NETWORKS` |
| `CDN` | `contains` | `APPLICATIONS` |
| `NETWORKS` | `contains` | `IPV6_ADDRESS` |
| `APPLICATIONS` | `contains` | `SERVICE` |
| `IPV6_ADDRESS` | `contains` | `TRANSPORT` |
| `TRANSPORT` | `contains` | `PORT` |
| `SERVICE` | `listens-to` | `PORT` |
| `SERVICE` | `had` | `SERVICE_VERSION` |
| `SERVICE` | `had` | `HTTP_STATUS_CODE` |
| `SERVICE` | `had` | `TLS_ENABLED` |
| `SERVICE` | `contains` | `SOFTWARE_USED` |
| `SOFTWARE_USED` | `had` | `ORIGIN_FINGERPRINT_SUPPRESSED` |
| `SERVICE` | `contains` | `CPE_URL` |
| `NETWORKS` | `contains` | `IPV4_ADDRESS` |
| `IPV4_ADDRESS` | `contains` | `TRANSPORT` |
---

*OS-Intel Scan*
