# Netdiscover scan narrative — `local_subnet_active_text`

## Introduction

This report narrates findings from a Netdiscover ARP discovery run. The story follows the scan metadata and each discovered system with its networks inventory (IPv4, MAC, vendor). This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `netdiscover — A — active ARP scan 192.168.1.0/24 (interactive text)`). Linked structures: `SCAN_CLI`, `SCAN_TIMESTAMP`, `SCAN_END_TIME`, `SCAN_SUMMARY`, `SCAN_EXIT_STATUS`, `SCAN_TRIES`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_timestamp_3["SCAN_TIMESTAMP"]
  scan_record_1 -->|had| scan_timestamp_3
  scan_end_time_4["SCAN_END_TIME"]
  scan_record_1 -->|had| scan_end_time_4
  scan_summary_5["SCAN_SUMMARY"]
  scan_record_1 -->|had| scan_summary_5
  scan_exit_status_6["SCAN_EXIT_STATUS"]
  scan_record_1 -->|had| scan_exit_status_6
  scan_tries_7["SCAN_TRIES"]
  scan_record_1 -->|had| scan_tries_7
  scan_empty_scans_8["SCAN_EMPTY_SCANS"]
  scan_record_1 -->|had| scan_empty_scans_8
  scan_discovered_9["SCAN_DISCOVERED"]
  scan_record_1 -->|had| scan_discovered_9
```

### Scan descriptors

| Nugget | Value |
| --- | --- |
| `SCAN_RECORD` | `netdiscover — A — active ARP scan 192.168.1.0/24 (interactive text)` |

## System

When only L2/L3 identity is known, emit SYSTEM (not HOST) with a NETWORKS category. This scan includes **12** System root node(s) (e.g. `192.168.1.1`, `192.168.1.10`, `192.168.1.14`). Linked structures: `NETWORKS`.

### Structure overview

```mermaid
flowchart TD
  system_1["SYSTEM"]
  networks_2["NETWORKS"]
  system_1 -->|contains| networks_2
```

### `NETWORKS`

```mermaid
flowchart TD
  networks_1["NETWORKS"]
  ipv4_address_2["IPV4_ADDRESS: 192.168.1.1"]
  networks_1 -->|contains| ipv4_address_2
  ipv4_address_3["IPV4_ADDRESS: 192.168.1.10"]
  networks_1 -->|contains| ipv4_address_3
  ipv4_address_4["IPV4_ADDRESS: 192.168.1.14"]
  networks_1 -->|contains| ipv4_address_4
  more_5["+21 more"]
  networks_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `192.168.1.1` |
| `IPV4_ADDRESS` | `192.168.1.10` |
| `IPV4_ADDRESS` | `192.168.1.14` |
| `IPV4_ADDRESS` | `192.168.1.15` |
| `IPV4_ADDRESS` | `192.168.1.16` |
| `IPV4_ADDRESS` | `192.168.1.2` |
| `IPV4_ADDRESS` | `192.168.1.250` |
| `IPV4_ADDRESS` | `192.168.1.3` |
| `IPV4_ADDRESS` | `192.168.1.4` |
| `IPV4_ADDRESS` | `192.168.1.6` |
| `IPV4_ADDRESS` | `192.168.1.7` |
| `IPV4_ADDRESS` | `192.168.1.8` |
| `MAC_ADDRESS` | `02:0f:b5:0a:e3:6c` |
| `MAC_ADDRESS` | `02:0f:b5:23:c6:49` |
| `MAC_ADDRESS` | `02:0f:b5:2f:b0:73` |
| `MAC_ADDRESS` | `02:0f:b5:46:32:8f` |
| `MAC_ADDRESS` | `02:0f:b5:b0:a8:79` |
| `MAC_ADDRESS` | `02:0f:b5:b7:bd:29` |
| `MAC_ADDRESS` | `14:5f:94:d8:7a:5f` |
| `MAC_ADDRESS` | `3c:a3:08:a4:d1:8d` |
| `MAC_ADDRESS` | `3e:48:b2:24:45:34` |
| `MAC_ADDRESS` | `5a:ba:45:91:e3:41` |
| `MAC_ADDRESS` | `88:d8:2e:c2:2c:0c` |
| `MAC_ADDRESS` | `cc:c7:60:67:89:48` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `192.168.1.1` |
| `IPV4_ADDRESS` | `192.168.1.10` |
| `IPV4_ADDRESS` | `192.168.1.14` |
| `IPV4_ADDRESS` | `192.168.1.15` |
| `IPV4_ADDRESS` | `192.168.1.16` |
| `IPV4_ADDRESS` | `192.168.1.2` |
| `IPV4_ADDRESS` | `192.168.1.250` |
| `IPV4_ADDRESS` | `192.168.1.3` |
| `IPV4_ADDRESS` | `192.168.1.4` |
| `IPV4_ADDRESS` | `192.168.1.6` |
| `IPV4_ADDRESS` | `192.168.1.7` |
| `IPV4_ADDRESS` | `192.168.1.8` |
| `MAC_ADDRESS` | `02:0f:b5:0a:e3:6c` |
| `MAC_ADDRESS` | `02:0f:b5:23:c6:49` |
| `MAC_ADDRESS` | `02:0f:b5:2f:b0:73` |
| `MAC_ADDRESS` | `02:0f:b5:46:32:8f` |
| `MAC_ADDRESS` | `02:0f:b5:b0:a8:79` |
| `MAC_ADDRESS` | `02:0f:b5:b7:bd:29` |
| `MAC_ADDRESS` | `14:5f:94:d8:7a:5f` |
| `MAC_ADDRESS` | `3c:a3:08:a4:d1:8d` |
| `MAC_ADDRESS` | `3e:48:b2:24:45:34` |
| `MAC_ADDRESS` | `5a:ba:45:91:e3:41` |
| `MAC_ADDRESS` | `88:d8:2e:c2:2c:0c` |
| `MAC_ADDRESS` | `cc:c7:60:67:89:48` |
| `MAC_VENDOR` | `Unknown` |
| `NETWORKS` | `networks:192.168.1.1` |
| `NETWORKS` | `networks:192.168.1.10` |
| `NETWORKS` | `networks:192.168.1.14` |
| `NETWORKS` | `networks:192.168.1.15` |
| `NETWORKS` | `networks:192.168.1.16` |
| `NETWORKS` | `networks:192.168.1.2` |
| `NETWORKS` | `networks:192.168.1.250` |
| `NETWORKS` | `networks:192.168.1.3` |
| `NETWORKS` | `networks:192.168.1.4` |
| `NETWORKS` | `networks:192.168.1.6` |
| `NETWORKS` | `networks:192.168.1.7` |
| `NETWORKS` | `networks:192.168.1.8` |
| `SCAN_CLI` | `netdiscover — A — active ARP scan 192.168.1.0/24 (interactive text)` |
| `SCAN_DISCOVERED` | `12` |
| `SCAN_EMPTY_SCANS` | `3` |
| `SCAN_END_TIME` | `Sun Aug 09 15:43:59 2026` |
| `SCAN_EXIT_STATUS` | `success` |
| `SCAN_RECORD` | `netdiscover — A — active ARP scan 192.168.1.0/24 (interactive text)` |
| `SCAN_SUMMARY` | `NetDiscover done at Sun Aug 09 15:43:59 2026; 12 Systems Discovered, 5 Scan Tries, 3 Empty Scans, scanned in 15.81 seconds` |
| `SCAN_TIMESTAMP` | `Sun Aug 09 15:43:43 2026` |
| `SCAN_TRIES` | `5` |
| `SYSTEM` | `192.168.1.1` |
| `SYSTEM` | `192.168.1.10` |
| `SYSTEM` | `192.168.1.14` |
| `SYSTEM` | `192.168.1.15` |
| `SYSTEM` | `192.168.1.16` |
| `SYSTEM` | `192.168.1.2` |
| `SYSTEM` | `192.168.1.250` |
| `SYSTEM` | `192.168.1.3` |
| `SYSTEM` | `192.168.1.4` |
| `SYSTEM` | `192.168.1.6` |
| `SYSTEM` | `192.168.1.7` |
| `SYSTEM` | `192.168.1.8` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TIMESTAMP` |
| `SCAN_RECORD` | `had` | `SCAN_END_TIME` |
| `SCAN_RECORD` | `had` | `SCAN_SUMMARY` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TRIES` |
| `SCAN_RECORD` | `had` | `SCAN_EMPTY_SCANS` |
| `SCAN_RECORD` | `had` | `SCAN_DISCOVERED` |
| `SCAN_RECORD` | `contains` | `SYSTEM` |
| `SYSTEM` | `contains` | `NETWORKS` |
| `NETWORKS` | `contains` | `IPV4_ADDRESS` |
| `NETWORKS` | `contains` | `MAC_ADDRESS` |
| `MAC_ADDRESS` | `had` | `MAC_VENDOR` |
---

*OS-Intel Scan*
