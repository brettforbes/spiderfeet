# Nerva scan narrative — `tcp_closed_clean_miss`

## Introduction

The scan used Nerva. Findings are organised under each meta-concept present in the graph (ENVIRONMENT, NETWORKS, APPLICATIONS, VULNERABILITIES, SECURITY). This report follows Scan → Host/System → Trace → Appendix. This report follows Scan → Host/System/Organisation/Domain (categories) → Trace → Appendix. Overview diagrams show ontology types and relations; category diagrams show a few example values with the rest in tables; the appendix inventories every node and edge.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `nerva:scanme.nmap.org:1:2026-06-30T07:40:54.267267+00:00`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`, `SCAN_TOOL`.

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
  scan_cli_2["SCAN_CLI: nerva -t scanme.nmap.org:1 --json -w 30…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nerva -t scanme.nmap.org:1 --json -w 3000` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: scanme.nmap.org:1"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `scanme.nmap.org:1` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-06-30T07:40:54.267267+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-06-30T07:40:54.267267+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 4.641"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `4.641` |

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

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `nerva -t scanme.nmap.org:1 --json -w 3000` |
| `SCAN_ELAPSED` | `4.641` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_RECORD` | `nerva:scanme.nmap.org:1:2026-06-30T07:40:54.267267+00:00` |
| `SCAN_START` | `2026-06-30T07:40:54.267267+00:00` |
| `SCAN_TARGET` | `scanme.nmap.org:1` |
| `SCAN_TOOL` | `nerva` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
---

*OS-Intel Scan*
