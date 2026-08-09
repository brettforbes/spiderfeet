# Nmap scan narrative — `tcp_top_ports_local_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:192.168.1.0/24:Fri Jun 26 04:00:30 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

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

### Scan descriptors

| Nugget | Value |
| --- | --- |
| `SCAN_RECORD` | `nmap:192.168.1.0/24:Fri Jun 26 04:00:30 2026` |

## Host

Qualified HOST endpoints own category trees for networks, applications, environment, and security findings. This scan includes **2** Host root node(s) (e.g. `192.168.1.9`, `192.168.1.11`). Linked structures: `NETWORKS`, `APPLICATIONS`.

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
  ipv4_address_2["IPV4_ADDRESS: 192.168.1.11"]
  networks_1 -->|contains| ipv4_address_2
  ipv4_address_3["IPV4_ADDRESS: 192.168.1.9"]
  networks_1 -->|contains| ipv4_address_3
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `192.168.1.11` |
| `IPV4_ADDRESS` | `192.168.1.9` |

### `APPLICATIONS`

```mermaid
flowchart TD
  applications_1["APPLICATIONS"]
  service_2["SERVICE: http-alt"]
  applications_1 -->|contains| service_2
  service_3["SERVICE: microsoft-ds"]
  applications_1 -->|contains| service_3
  service_4["SERVICE: msrpc"]
  applications_1 -->|contains| service_4
  more_5["+2 more"]
  applications_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http-alt` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `ppp` |

### `ENVIRONMENT`

```mermaid
flowchart TD
  environment_1["ENVIRONMENT"]
  applications_2["APPLICATIONS: applications:192.168.1.11"]
  environment_1 -->|contains| applications_2
  applications_3["APPLICATIONS: applications:192.168.1.9"]
  environment_1 -->|contains| applications_3
  host_status_4["HOST_STATUS: up"]
  environment_1 -->|contains| host_status_4
  more_5["+4 more"]
  environment_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:192.168.1.11` |
| `APPLICATIONS` | `applications:192.168.1.9` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `localhost-response` |
| `INTERNET_NAME` | `host.docker.internal` |
| `NETWORKS` | `networks:192.168.1.11` |
| `NETWORKS` | `networks:192.168.1.9` |

### `VULNERABILITIES`

```mermaid
flowchart TD
  vulnerabilities_1["VULNERABILITIES"]
  applications_2["APPLICATIONS: applications:192.168.1.11"]
  vulnerabilities_1 -->|contains| applications_2
  applications_3["APPLICATIONS: applications:192.168.1.9"]
  vulnerabilities_1 -->|contains| applications_3
  host_status_4["HOST_STATUS: up"]
  vulnerabilities_1 -->|contains| host_status_4
  more_5["+4 more"]
  vulnerabilities_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:192.168.1.11` |
| `APPLICATIONS` | `applications:192.168.1.9` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `localhost-response` |
| `INTERNET_NAME` | `host.docker.internal` |
| `NETWORKS` | `networks:192.168.1.11` |
| `NETWORKS` | `networks:192.168.1.9` |

### `SECURITY`

```mermaid
flowchart TD
  security_1["SECURITY"]
  applications_2["APPLICATIONS: applications:192.168.1.11"]
  security_1 -->|contains| applications_2
  applications_3["APPLICATIONS: applications:192.168.1.9"]
  security_1 -->|contains| applications_3
  host_status_4["HOST_STATUS: up"]
  security_1 -->|contains| host_status_4
  more_5["+4 more"]
  security_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:192.168.1.11` |
| `APPLICATIONS` | `applications:192.168.1.9` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `localhost-response` |
| `INTERNET_NAME` | `host.docker.internal` |
| `NETWORKS` | `networks:192.168.1.11` |
| `NETWORKS` | `networks:192.168.1.9` |

## Services and ports

APPLICATION services listen-to PORT entities under NETWORKS/TRANSPORT. This scan includes **5** Services and ports root node(s) (e.g. `msrpc`, `netbios-ssn`, `microsoft-ds`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  service_1["SERVICE"]
```

### Values

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http-alt` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `ppp` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:192.168.1.11` |
| `APPLICATIONS` | `applications:192.168.1.9` |
| `HOST` | `192.168.1.11` |
| `HOST` | `192.168.1.9` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `localhost-response` |
| `INTERNET_NAME` | `host.docker.internal` |
| `IPV4_ADDRESS` | `192.168.1.11` |
| `IPV4_ADDRESS` | `192.168.1.9` |
| `NETWORKS` | `networks:192.168.1.11` |
| `NETWORKS` | `networks:192.168.1.9` |
| `PORT` | `135` |
| `PORT` | `139` |
| `PORT` | `3000` |
| `PORT` | `445` |
| `PORT` | `8000` |
| `PORT_PROTOCOL` | `tcp` |
| `PORT_STATE` | `open` |
| `PORT_STATE_REASON` | `syn-ack` |
| `SCAN_CLI` | `nmap -sT -T3 --top-ports 100 --open -oX - 192.168.1.0/24` |
| `SCAN_ELAPSED` | `21.75` |
| `SCAN_RECORD` | `nmap:192.168.1.0/24:Fri Jun 26 04:00:30 2026` |
| `SCAN_START` | `Fri Jun 26 04:00:30 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 04:00:52 2026; 256 IP addresses (2 hosts up) scanned in 21.75 seconds` |
| `SCAN_TARGET` | `192.168.1.0/24` |
| `SCAN_TOOL` | `nmap` |
| `SCAN_VERSION` | `7.80` |
| `SERVICE` | `http-alt` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `ppp` |
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
