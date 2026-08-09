# Httpx scan narrative — `from_subfinder_invalid_clean_miss`

## Introduction

Httpx confirms live web endpoints, HTTP metadata, and technology signals for each probed host under the 10 H0-H7 ruleset.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `httpx:not-a-real-domain-xyzzy.invalid:httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_invalid_clean_miss_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_invalid_clean_miss.jsonl -silent -threads 2 -timeout 10`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_PROBE_PROFILE`, `SCAN_HOST_INPUT_COUNT`, `SCAN_START`, `SCAN_ELAPSED`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_target_3["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_3
  scan_probe_profile_4["SCAN_PROBE_PROFILE"]
  scan_record_1 -->|had| scan_probe_profile_4
  scan_host_input_count_5["SCAN_HOST_INPUT_COUNT"]
  scan_record_1 -->|had| scan_host_input_count_5
  scan_start_6["SCAN_START"]
  scan_record_1 -->|had| scan_start_6
  scan_elapsed_7["SCAN_ELAPSED"]
  scan_record_1 -->|had| scan_elapsed_7
  scan_exit_status_8["SCAN_EXIT_STATUS"]
  scan_record_1 -->|had| scan_exit_status_8
  scan_tool_9["SCAN_TOOL"]
  scan_record_1 -->|had| scan_tool_9
  upstream_scenario_id_10["UPSTREAM_SCENARIO_ID"]
  scan_record_1 -->|had| upstream_scenario_id_10
```

### `SCAN_CLI`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI: httpx -l .docs/docs-for-cli-tools/explo…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_invalid_clean_miss_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_invalid_clean_miss.jsonl -silent -threads 2 -timeout 10` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: not-a-real-domain-xyzzy.invalid"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `not-a-real-domain-xyzzy.invalid` |

### `SCAN_PROBE_PROFILE`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_probe_profile_2["SCAN_PROBE_PROFILE: status-code,title,tech-detect,server,cd…"]
  scan_record_1 -->|contains| scan_probe_profile_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_PROBE_PROFILE` | `status-code,title,tech-detect,server,cdn,ip` |

### `SCAN_HOST_INPUT_COUNT`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_host_input_count_2["SCAN_HOST_INPUT_COUNT: 1"]
  scan_record_1 -->|contains| scan_host_input_count_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_HOST_INPUT_COUNT` | `1` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-07-05T16:06:13.333301+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-05T16:06:13.333301+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 1.688"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `1.688` |

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
  scan_tool_2["SCAN_TOOL: httpx"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `httpx` |

### `UPSTREAM_SCENARIO_ID`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  upstream_scenario_id_2["UPSTREAM_SCENARIO_ID: invalid_domain_clean_miss"]
  scan_record_1 -->|contains| upstream_scenario_id_2
```

| Nugget | Value |
| --- | --- |
| `UPSTREAM_SCENARIO_ID` | `invalid_domain_clean_miss` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **1** Domains root node(s) (e.g. `not-a-real-domain-xyzzy.invalid`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### Values

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `not-a-real-domain-xyzzy.invalid` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `not-a-real-domain-xyzzy.invalid` |
| `HTTP_LIVENESS_STATUS` | `unconfirmed` |
| `SCAN_CLI` | `httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_invalid_clean_miss_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_invalid_clean_miss.jsonl -silent -threads 2 -timeout 10` |
| `SCAN_ELAPSED` | `1.688` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_HOST_INPUT_COUNT` | `1` |
| `SCAN_PROBE_PROFILE` | `status-code,title,tech-detect,server,cdn,ip` |
| `SCAN_RECORD` | `httpx:not-a-real-domain-xyzzy.invalid:httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_invalid_clean_miss_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_invalid_clean_miss.jsonl -silent -threads 2 -timeout 10` |
| `SCAN_START` | `2026-07-05T16:06:13.333301+00:00` |
| `SCAN_TARGET` | `not-a-real-domain-xyzzy.invalid` |
| `SCAN_TOOL` | `httpx` |
| `UPSTREAM_SCENARIO_ID` | `invalid_domain_clean_miss` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_PROBE_PROFILE` |
| `SCAN_RECORD` | `had` | `SCAN_HOST_INPUT_COUNT` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `DOMAIN_NAME` |
| `SCAN_RECORD` | `had` | `UPSTREAM_SCENARIO_ID` |
| `DOMAIN_NAME` | `had` | `HTTP_LIVENESS_STATUS` |
---

*OS-Intel Scan*
