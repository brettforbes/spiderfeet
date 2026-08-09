# Nmap scan narrative — `host_discovery_permissive_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:scanme.nmap.org:Fri Jun 26 03:51:03 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

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
| `SCAN_RECORD` | `nmap:scanme.nmap.org:Fri Jun 26 03:51:03 2026` |

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
```

_No values._

### `ENVIRONMENT`

```mermaid
flowchart TD
  environment_1["ENVIRONMENT"]
  applications_2["APPLICATIONS: applications:45.33.32.156"]
  environment_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  environment_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: echo-reply"]
  environment_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  environment_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:45.33.32.156` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `echo-reply` |
| `INTERNET_NAME` | `scanme.nmap.org` |
| `NETWORKS` | `networks:45.33.32.156` |

### `VULNERABILITIES`

```mermaid
flowchart TD
  vulnerabilities_1["VULNERABILITIES"]
  applications_2["APPLICATIONS: applications:45.33.32.156"]
  vulnerabilities_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  vulnerabilities_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: echo-reply"]
  vulnerabilities_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  vulnerabilities_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:45.33.32.156` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `echo-reply` |
| `INTERNET_NAME` | `scanme.nmap.org` |
| `NETWORKS` | `networks:45.33.32.156` |

### `SECURITY`

```mermaid
flowchart TD
  security_1["SECURITY"]
  applications_2["APPLICATIONS: applications:45.33.32.156"]
  security_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  security_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: echo-reply"]
  security_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  security_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:45.33.32.156` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `echo-reply` |
| `INTERNET_NAME` | `scanme.nmap.org` |
| `NETWORKS` | `networks:45.33.32.156` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:45.33.32.156` |
| `HOST` | `45.33.32.156` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `echo-reply` |
| `INTERNET_NAME` | `scanme.nmap.org` |
| `IPV4_ADDRESS` | `45.33.32.156` |
| `NETWORKS` | `networks:45.33.32.156` |
| `SCAN_CLI` | `nmap -sn -T3 -oX - scanme.nmap.org` |
| `SCAN_ELAPSED` | `0.94` |
| `SCAN_RECORD` | `nmap:scanme.nmap.org:Fri Jun 26 03:51:03 2026` |
| `SCAN_START` | `Fri Jun 26 03:51:03 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 03:51:04 2026; 1 IP address (1 host up) scanned in 0.94 seconds` |
| `SCAN_TARGET` | `scanme.nmap.org` |
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
