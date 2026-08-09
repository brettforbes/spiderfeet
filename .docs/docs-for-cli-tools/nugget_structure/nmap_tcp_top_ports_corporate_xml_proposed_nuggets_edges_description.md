# Nmap scan narrative — `tcp_top_ports_corporate_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:bbc.co.uk:Fri Jun 26 03:59:31 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

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
| `SCAN_RECORD` | `nmap:bbc.co.uk:Fri Jun 26 03:59:31 2026` |

## Host

Qualified HOST endpoints own category trees for networks, applications, environment, and security findings. This scan includes **1** Host root node(s) (e.g. `151.101.128.81`). Linked structures: `NETWORKS`, `APPLICATIONS`.

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
  ipv4_address_2["IPV4_ADDRESS: 151.101.128.81"]
  networks_1 -->|contains| ipv4_address_2
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `151.101.128.81` |

### `APPLICATIONS`

```mermaid
flowchart TD
  applications_1["APPLICATIONS"]
  service_2["SERVICE: domain"]
  applications_1 -->|contains| service_2
  service_3["SERVICE: ftp"]
  applications_1 -->|contains| service_3
  service_4["SERVICE: http"]
  applications_1 -->|contains| service_4
  more_5["+17 more"]
  applications_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `SERVICE` | `domain` |
| `SERVICE` | `ftp` |
| `SERVICE` | `http` |
| `SERVICE` | `http-proxy` |
| `SERVICE` | `https` |
| `SERVICE` | `imap` |
| `SERVICE` | `imaps` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `ms-wbt-server` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `mysql` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `pop3` |
| `SERVICE` | `pop3s` |
| `SERVICE` | `pptp` |
| `SERVICE` | `rpcbind` |
| `SERVICE` | `smtp` |
| `SERVICE` | `ssh` |
| `SERVICE` | `telnet` |
| `SERVICE` | `vnc` |

### `ENVIRONMENT`

```mermaid
flowchart TD
  environment_1["ENVIRONMENT"]
  applications_2["APPLICATIONS: applications:151.101.128.81"]
  environment_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  environment_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: syn-ack"]
  environment_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  environment_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:151.101.128.81` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `syn-ack` |
| `INTERNET_NAME` | `bbc.co.uk` |
| `NETWORKS` | `networks:151.101.128.81` |

### `VULNERABILITIES`

```mermaid
flowchart TD
  vulnerabilities_1["VULNERABILITIES"]
  applications_2["APPLICATIONS: applications:151.101.128.81"]
  vulnerabilities_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  vulnerabilities_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: syn-ack"]
  vulnerabilities_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  vulnerabilities_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:151.101.128.81` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `syn-ack` |
| `INTERNET_NAME` | `bbc.co.uk` |
| `NETWORKS` | `networks:151.101.128.81` |

### `SECURITY`

```mermaid
flowchart TD
  security_1["SECURITY"]
  applications_2["APPLICATIONS: applications:151.101.128.81"]
  security_1 -->|contains| applications_2
  host_status_3["HOST_STATUS: up"]
  security_1 -->|contains| host_status_3
  host_status_reason_4["HOST_STATUS_REASON: syn-ack"]
  security_1 -->|contains| host_status_reason_4
  more_5["+2 more"]
  security_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:151.101.128.81` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `syn-ack` |
| `INTERNET_NAME` | `bbc.co.uk` |
| `NETWORKS` | `networks:151.101.128.81` |

## Services and ports

APPLICATION services listen-to PORT entities under NETWORKS/TRANSPORT. This scan includes **20** Services and ports root node(s) (e.g. `ftp`, `ssh`, `telnet`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  service_1["SERVICE"]
```

### Values

| Nugget | Value |
| --- | --- |
| `SERVICE` | `domain` |
| `SERVICE` | `ftp` |
| `SERVICE` | `http` |
| `SERVICE` | `http-proxy` |
| `SERVICE` | `https` |
| `SERVICE` | `imap` |
| `SERVICE` | `imaps` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `ms-wbt-server` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `mysql` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `pop3` |
| `SERVICE` | `pop3s` |
| `SERVICE` | `pptp` |
| `SERVICE` | `rpcbind` |
| `SERVICE` | `smtp` |
| `SERVICE` | `ssh` |
| `SERVICE` | `telnet` |
| `SERVICE` | `vnc` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `applications:151.101.128.81` |
| `HOST` | `151.101.128.81` |
| `HOST_STATUS` | `up` |
| `HOST_STATUS_REASON` | `syn-ack` |
| `INTERNET_NAME` | `bbc.co.uk` |
| `IPV4_ADDRESS` | `151.101.128.81` |
| `NETWORKS` | `networks:151.101.128.81` |
| `PORT` | `110` |
| `PORT` | `111` |
| `PORT` | `135` |
| `PORT` | `139` |
| `PORT` | `143` |
| `PORT` | `1723` |
| `PORT` | `21` |
| `PORT` | `22` |
| `PORT` | `23` |
| `PORT` | `25` |
| `PORT` | `3306` |
| `PORT` | `3389` |
| `PORT` | `443` |
| `PORT` | `445` |
| `PORT` | `53` |
| `PORT` | `5900` |
| `PORT` | `80` |
| `PORT` | `8080` |
| `PORT` | `993` |
| `PORT` | `995` |
| `PORT_PROTOCOL` | `tcp` |
| `PORT_STATE` | `filtered` |
| `PORT_STATE` | `open` |
| `PORT_STATE_REASON` | `no-response` |
| `PORT_STATE_REASON` | `syn-ack` |
| `SCAN_CLI` | `nmap -sT -T3 --top-ports 20 -oX - bbc.co.uk` |
| `SCAN_ELAPSED` | `2.33` |
| `SCAN_RECORD` | `nmap:bbc.co.uk:Fri Jun 26 03:59:31 2026` |
| `SCAN_START` | `Fri Jun 26 03:59:31 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 03:59:33 2026; 1 IP address (1 host up) scanned in 2.33 seconds` |
| `SCAN_TARGET` | `bbc.co.uk` |
| `SCAN_TOOL` | `nmap` |
| `SCAN_VERSION` | `7.80` |
| `SERVICE` | `domain` |
| `SERVICE` | `ftp` |
| `SERVICE` | `http` |
| `SERVICE` | `http-proxy` |
| `SERVICE` | `https` |
| `SERVICE` | `imap` |
| `SERVICE` | `imaps` |
| `SERVICE` | `microsoft-ds` |
| `SERVICE` | `ms-wbt-server` |
| `SERVICE` | `msrpc` |
| `SERVICE` | `mysql` |
| `SERVICE` | `netbios-ssn` |
| `SERVICE` | `pop3` |
| `SERVICE` | `pop3s` |
| `SERVICE` | `pptp` |
| `SERVICE` | `rpcbind` |
| `SERVICE` | `smtp` |
| `SERVICE` | `ssh` |
| `SERVICE` | `telnet` |
| `SERVICE` | `vnc` |
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
