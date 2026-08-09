# Subfinder scan narrative — `corporate_k2am_passive_cs`

## Introduction

Subfinder contributes DNS-focused domain enumeration. Active-mode IP resolution is retained as an IPV4_ADDRESS fact using currently approved SPEC-004 relations; the exact dns-resolves-to relation remains deferred until relation coverage is updated.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `subfinder:k2am.com.au:subfinder -d k2am.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_k2am_passive_cs.jsonl -silent`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_MODE`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`.

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
  scan_cli_2["SCAN_CLI: subfinder -d k2am.com.au -oJ -cs -o .do…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `subfinder -d k2am.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_k2am_passive_cs.jsonl -silent` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: k2am.com.au"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `k2am.com.au` |

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
  scan_start_2["SCAN_START: 2026-07-05T14:24:52.891526+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-05T14:24:52.891526+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 23.594"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `23.594` |

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

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **19** Domains root node(s) (e.g. `k2am.com.au`, `link.k2am.com.au`, `owa.k2am.com.au`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### Values

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `apps.k2am.com.au` |
| `DOMAIN_NAME` | `cpanel.k2am.com.au` |
| `DOMAIN_NAME` | `cpcalendars.k2am.com.au` |
| `DOMAIN_NAME` | `cpcontacts.k2am.com.au` |
| `DOMAIN_NAME` | `k2am.com.au` |
| `DOMAIN_NAME` | `kii.k2am.com.au` |
| `DOMAIN_NAME` | `ksm.k2am.com.au` |
| `DOMAIN_NAME` | `link.k2am.com.au` |
| `DOMAIN_NAME` | `mail.k2am.com.au` |
| `DOMAIN_NAME` | `owa.k2am.com.au` |
| `DOMAIN_NAME` | `smtp1.k2am.com.au` |
| `DOMAIN_NAME` | `smtp2.k2am.com.au` |
| `DOMAIN_NAME` | `webdisk.k2am.com.au` |
| `DOMAIN_NAME` | `webmail.k2am.com.au` |
| `DOMAIN_NAME` | `www.apps.k2am.com.au` |
| `DOMAIN_NAME` | `www.k2am.com.au` |
| `DOMAIN_NAME` | `www.kii.k2am.com.au` |
| `DOMAIN_NAME` | `www.ksm.k2am.com.au` |
| `DOMAIN_NAME` | `www.owa.k2am.com.au` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `DISCOVERY_MODE` | `passive` |
| `DISCOVERY_SOURCE` | `crtsh` |
| `DISCOVERY_SOURCE` | `hackertarget` |
| `DOMAIN_NAME` | `apps.k2am.com.au` |
| `DOMAIN_NAME` | `cpanel.k2am.com.au` |
| `DOMAIN_NAME` | `cpcalendars.k2am.com.au` |
| `DOMAIN_NAME` | `cpcontacts.k2am.com.au` |
| `DOMAIN_NAME` | `k2am.com.au` |
| `DOMAIN_NAME` | `kii.k2am.com.au` |
| `DOMAIN_NAME` | `ksm.k2am.com.au` |
| `DOMAIN_NAME` | `link.k2am.com.au` |
| `DOMAIN_NAME` | `mail.k2am.com.au` |
| `DOMAIN_NAME` | `owa.k2am.com.au` |
| `DOMAIN_NAME` | `smtp1.k2am.com.au` |
| `DOMAIN_NAME` | `smtp2.k2am.com.au` |
| `DOMAIN_NAME` | `webdisk.k2am.com.au` |
| `DOMAIN_NAME` | `webmail.k2am.com.au` |
| `DOMAIN_NAME` | `www.apps.k2am.com.au` |
| `DOMAIN_NAME` | `www.k2am.com.au` |
| `DOMAIN_NAME` | `www.kii.k2am.com.au` |
| `DOMAIN_NAME` | `www.ksm.k2am.com.au` |
| `DOMAIN_NAME` | `www.owa.k2am.com.au` |
| `DOMAIN_NAME_PARENT` | `apps.k2am.com.au` |
| `DOMAIN_NAME_PARENT` | `com.au` |
| `DOMAIN_NAME_PARENT` | `k2am.com.au` |
| `DOMAIN_NAME_PARENT` | `kii.k2am.com.au` |
| `DOMAIN_NAME_PARENT` | `ksm.k2am.com.au` |
| `DOMAIN_NAME_PARENT` | `owa.k2am.com.au` |
| `LIVENESS_STATUS` | `unconfirmed` |
| `SCAN_CLI` | `subfinder -d k2am.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_k2am_passive_cs.jsonl -silent` |
| `SCAN_ELAPSED` | `23.594` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_MODE` | `passive` |
| `SCAN_RECORD` | `subfinder:k2am.com.au:subfinder -d k2am.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_k2am_passive_cs.jsonl -silent` |
| `SCAN_START` | `2026-07-05T14:24:52.891526+00:00` |
| `SCAN_TARGET` | `k2am.com.au` |
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
