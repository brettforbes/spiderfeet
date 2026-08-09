# Nmap scan narrative — `windows_enrich_local_xml`

## Introduction

This report narrates findings from a Nmap scan. The story follows the scan record, each discovered host (networks, applications, environment), and any traceroute path. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nmap:192.168.1.12:Fri Jun 26 04:01:18 2026`). Linked structures: `SCAN_CLI`, `SCAN_VERSION`, `SCAN_START`, `SCAN_TARGET`, `SCAN_SUMMARY`, `SCAN_ELAPSED`.

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
  scan_cli_2["SCAN_CLI: nmap -sT -sV -A -T3 -p 135,445,8000 -oX…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nmap -sT -sV -A -T3 -p 135,445,8000 -oX - 192.168.1.12` |

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
  scan_start_2["SCAN_START: Fri Jun 26 04:01:18 2026"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `Fri Jun 26 04:01:18 2026` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: 192.168.1.12"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `192.168.1.12` |

### `SCAN_SUMMARY`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_summary_2["SCAN_SUMMARY: Nmap done at Fri Jun 26 04:01:20 2026; …"]
  scan_record_1 -->|contains| scan_summary_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 04:01:20 2026; 1 IP address (0 hosts up) scanned in 2.49 seconds` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 2.49"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `2.49` |

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

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nmap -sT -sV -A -T3 -p 135,445,8000 -oX - 192.168.1.12` |
| `SCAN_ELAPSED` | `2.49` |
| `SCAN_RECORD` | `nmap:192.168.1.12:Fri Jun 26 04:01:18 2026` |
| `SCAN_START` | `Fri Jun 26 04:01:18 2026` |
| `SCAN_SUMMARY` | `Nmap done at Fri Jun 26 04:01:20 2026; 1 IP address (0 hosts up) scanned in 2.49 seconds` |
| `SCAN_TARGET` | `192.168.1.12` |
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
---

*OS-Intel Scan*
