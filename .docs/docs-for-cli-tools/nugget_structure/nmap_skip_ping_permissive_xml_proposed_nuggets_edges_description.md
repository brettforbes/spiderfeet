# Nmap scan narrative — `skip_ping_permissive_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:scanme.nmap.org:Fri Jun 26 03:56:03 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_version_3["SCAN_VERSION"]
  scan_record_1 -->|had| scan_version_3
  scan_start_4["SCAN_START"]
  scan_record_1 -->|had| scan_start_4
  scan_target_5["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_5
  scan_summary_6["SCAN_SUMMARY"]
  scan_record_1 -->|had| scan_summary_6
  scan_elapsed_7["SCAN_ELAPSED"]
  scan_record_1 -->|had| scan_elapsed_7
  scan_tool_8["SCAN_TOOL"]
  scan_record_1 -->|had| scan_tool_8
```

### `SCAN_CLI`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI: nmap -sT -Pn -T3 -p 80 -oX - scanme.nma…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nmap -sT -Pn -T3 -p 80 -oX - scanme.nmap.org` |

### `SCAN_VERSION`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_version_2["SCAN_VERSION: 7.80"]
  scan_record_1 -->|contains| scan_version_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_VERSION` | `7.80` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: Fri Jun 26 03:56:03 2026"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `Fri Jun 26 03:56:03 2026` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: scanme.nmap.org"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `scanme.nmap.org` |

### `SCAN_SUMMARY`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_summary_2["SCAN_SUMMARY: Nmap done at Fri Jun 26 03:56:03 2026; …"]
  scan_record_1 -->|contains| scan_summary_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 03:56:03 2026; 1 IP address (1 host up) scanned in 0.31 seconds` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 0.31"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `0.31` |

### `SCAN_TOOL`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_tool_2["SCAN_TOOL: nmap"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `nmap` |

## Host

Qualified HOST endpoints own category trees for networks, applications, environment, and security findings. This scan includes **1** Host root node(s) (e.g. `45.33.32.156`). Linked structures: `NETWORKS`, `APPLICATIONS`.

### Structure overview

```mermaid
flowchart TD
  host_1["HOST"]
  networks_2["NETWORKS"]
  host_1 -->|contains| networks_2
  applications_3["APPLICATIONS"]
  host_1 -->|contains| applications_3
```

### `NETWORKS`

```mermaid
flowchart TD
  networks_1["NETWORKS"]
  ipv4_address_2["IPV4_ADDRESS: 45.33.32.156"]
  networks_1 -->|contains| ipv4_address_2
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `45.33.32.156` |

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
| `APPLICATIONS` | `applications:45.33.32.156` |
| `HOST` | `45.33.32.156` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `user-set` |
| `INTERNET_NAME` | `scanme.nmap.org` |
| `IPV4_ADDRESS` | `45.33.32.156` |
| `NETWORKS` | `networks:45.33.32.156` |
| `PORT` | `80` |
| `PORT_PROTOCOL` | `tcp` |
| `PORT_STATE` | `open` |
| `PORT_STATE_REASON` | `syn-ack` |
| `SCAN_CLI` | `nmap -sT -Pn -T3 -p 80 -oX - scanme.nmap.org` |
| `SCAN_ELAPSED` | `0.31` |
| `SCAN_RECORD` | `nmap:scanme.nmap.org:Fri Jun 26 03:56:03 2026` |
| `SCAN_START` | `Fri Jun 26 03:56:03 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 03:56:03 2026; 1 IP address (1 host up) scanned in 0.31 seconds` |
| `SCAN_TARGET` | `scanme.nmap.org` |
| `SCAN_TOOL` | `nmap` |
| `SCAN_VERSION` | `7.80` |
| `SERVICE` | `http` |
| `TRANSPORT` | `tcp` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_VERSION` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_SUMMARY` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `HOST` |
| `HOST` | `had` | `HOST_STATUS` |
| `HOST` | `had` | `HOST_STATUS_REASON` |
| `HOST` | `had` | `INTERNET_NAME` |
| `HOST` | `contains` | `NETWORKS` |
| `NETWORKS` | `contains` | `IPV4_ADDRESS` |
| `HOST` | `contains` | `APPLICATIONS` |
| `IPV4_ADDRESS` | `contains` | `TRANSPORT` |
| `TRANSPORT` | `contains` | `PORT` |
| `PORT` | `had` | `PORT_STATE` |
| `PORT` | `had` | `PORT_STATE_REASON` |
| `PORT` | `had` | `PORT_PROTOCOL` |
| `APPLICATIONS` | `contains` | `SERVICE` |
| `SERVICE` | `listens-to` | `PORT` |
---

*OS-Intel Scan*
