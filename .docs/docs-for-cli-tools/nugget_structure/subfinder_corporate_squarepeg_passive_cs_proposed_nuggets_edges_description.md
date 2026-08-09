# Subfinder scan narrative — `corporate_squarepeg_passive_cs`

## Introduction

Subfinder contributes DNS-focused domain enumeration. Active-mode IP resolution is retained as an IPV4_ADDRESS fact using currently approved SPEC-004 relations; the exact dns-resolves-to relation remains deferred until relation coverage is updated.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `subfinder:squarepeg.vc:subfinder -d squarepeg.vc -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_squarepeg_passive_cs.jsonl -silent`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_MODE`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_target_3["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_3
  scan_mode_4["SCAN_MODE"]
  scan_record_1 -->|had| scan_mode_4
  scan_start_5["SCAN_START"]
  scan_record_1 -->|had| scan_start_5
  scan_elapsed_6["SCAN_ELAPSED"]
  scan_record_1 -->|had| scan_elapsed_6
  scan_exit_status_7["SCAN_EXIT_STATUS"]
  scan_record_1 -->|had| scan_exit_status_7
  scan_tool_8["SCAN_TOOL"]
  scan_record_1 -->|had| scan_tool_8
```

### `SCAN_CLI`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI: subfinder -d squarepeg.vc -oJ -cs -o .d…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `subfinder -d squarepeg.vc -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_squarepeg_passive_cs.jsonl -silent` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: squarepeg.vc"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `squarepeg.vc` |

### `SCAN_MODE`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_mode_2["SCAN_MODE: passive"]
  scan_record_1 -->|contains| scan_mode_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_MODE` | `passive` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-07-05T14:24:08.368569+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-05T14:24:08.368569+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 22.094"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `22.094` |

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
  scan_tool_2["SCAN_TOOL: subfinder"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `subfinder` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **8** Domains root node(s) (e.g. `squarepeg.vc`, `helix.squarepeg.vc`, `plus.squarepeg.vc`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### Values

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `plus.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `static.squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `DISCOVERY_MODE` | `passive` |
| `DISCOVERY_SOURCE` | `crtsh` |
| `DISCOVERY_SOURCE` | `hackertarget` |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `plus.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `static.squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |
| `DOMAIN_NAME_PARENT` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME_PARENT` | `squarepeg.vc` |
| `LIVENESS_STATUS` | `unconfirmed` |
| `SCAN_CLI` | `subfinder -d squarepeg.vc -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_squarepeg_passive_cs.jsonl -silent` |
| `SCAN_ELAPSED` | `22.094` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_MODE` | `passive` |
| `SCAN_RECORD` | `subfinder:squarepeg.vc:subfinder -d squarepeg.vc -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_squarepeg_passive_cs.jsonl -silent` |
| `SCAN_START` | `2026-07-05T14:24:08.368569+00:00` |
| `SCAN_TARGET` | `squarepeg.vc` |
| `SCAN_TOOL` | `subfinder` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_MODE` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `DOMAIN_NAME` |
| `DOMAIN_NAME` | `had` | `DOMAIN_NAME_PARENT` |
| `DOMAIN_NAME` | `had` | `DISCOVERY_MODE` |
| `DOMAIN_NAME` | `had` | `DISCOVERY_SOURCE` |
| `DOMAIN_NAME` | `had` | `LIVENESS_STATUS` |
---

*OS-Intel Scan*
