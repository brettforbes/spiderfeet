# Nmap scan narrative — `host_discovery_local_subnet_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:192.168.1.0/24:Fri Jun 26 04:00:07 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

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
| `SCAN_RECORD` | `nmap:192.168.1.0/24:Fri Jun 26 04:00:07 2026` |

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
```

_No values._

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
| `SCAN_CLI` | `nmap -sn -T3 -oX - 192.168.1.0/24` |
| `SCAN_ELAPSED` | `11.46` |
| `SCAN_RECORD` | `nmap:192.168.1.0/24:Fri Jun 26 04:00:07 2026` |
| `SCAN_START` | `Fri Jun 26 04:00:07 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 04:00:18 2026; 256 IP addresses (2 hosts up) scanned in 11.46 seconds` |
| `SCAN_TARGET` | `192.168.1.0/24` |
| `SCAN_TOOL` | `nmap` |
| `SCAN_VERSION` | `7.80` |

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
---

*OS-Intel Scan*
