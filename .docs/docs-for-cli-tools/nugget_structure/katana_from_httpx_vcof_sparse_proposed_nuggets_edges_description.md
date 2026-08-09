# Katana scan narrative — `from_httpx_vcof_sparse`

## Introduction

Katana emits internal linked URLs, host domains, and HTTP status/method descriptors for each crawled endpoint discovered from the seed target.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `katana:venturecapitalopportunitiesfund.com.au:katana -list .docs/docs-for-cli-tools/exploration_scratch/katana/urls/from_httpx_vcof_sparse_urls.txt -silent -jsonl -o .docs/docs-for-cli-tools/exploration_scratch/katana/exams/from_httpx_vcof_sparse.jsonl -depth 3 -c 5 -timeout 15 -fs fqdn -ct 3m`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_CRAWL_PROFILE`, `SCAN_URL_INPUT_COUNT`, `SCAN_START`, `SCAN_ELAPSED`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_target_3["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_3
  scan_crawl_profile_4["SCAN_CRAWL_PROFILE"]
  scan_record_1 -->|had| scan_crawl_profile_4
  scan_url_input_count_5["SCAN_URL_INPUT_COUNT"]
  scan_record_1 -->|had| scan_url_input_count_5
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
  scan_cli_2["SCAN_CLI: katana -list .docs/docs-for-cli-tools/e…"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `katana -list .docs/docs-for-cli-tools/exploration_scratch/katana/urls/from_httpx_vcof_sparse_urls.txt -silent -jsonl -o .docs/docs-for-cli-tools/exploration_scratch/katana/exams/from_httpx_vcof_sparse.jsonl -depth 3 -c 5 -timeout 15 -fs fqdn -ct 3m` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: venturecapitalopportunitiesfund.com.au"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `venturecapitalopportunitiesfund.com.au` |

### `SCAN_CRAWL_PROFILE`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_crawl_profile_2["SCAN_CRAWL_PROFILE: depth-3,fqdn-scope,concurrency-5,timeou…"]
  scan_record_1 -->|contains| scan_crawl_profile_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CRAWL_PROFILE` | `depth-3,fqdn-scope,concurrency-5,timeout-15,crawl-duration-3m` |

### `SCAN_URL_INPUT_COUNT`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_url_input_count_2["SCAN_URL_INPUT_COUNT: 1"]
  scan_record_1 -->|contains| scan_url_input_count_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_URL_INPUT_COUNT` | `1` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-07-06T11:25:46.218632+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-06T11:25:46.218632+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 705.719"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `705.719` |

### `SCAN_EXIT_STATUS`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_exit_status_2["SCAN_EXIT_STATUS: 124"]
  scan_record_1 -->|contains| scan_exit_status_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_EXIT_STATUS` | `124` |

### `SCAN_TOOL`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_tool_2["SCAN_TOOL: katana"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `katana` |

### `UPSTREAM_SCENARIO_ID`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  upstream_scenario_id_2["UPSTREAM_SCENARIO_ID: from_subfinder_vcof_sparse"]
  scan_record_1 -->|contains| upstream_scenario_id_2
```

| Nugget | Value |
| --- | --- |
| `UPSTREAM_SCENARIO_ID` | `from_subfinder_vcof_sparse` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **1** Domains root node(s) (e.g. `venturecapitalopportunitiesfund.com.au`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### Values

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `venturecapitalopportunitiesfund.com.au` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `venturecapitalopportunitiesfund.com.au` |
| `SCAN_CLI` | `katana -list .docs/docs-for-cli-tools/exploration_scratch/katana/urls/from_httpx_vcof_sparse_urls.txt -silent -jsonl -o .docs/docs-for-cli-tools/exploration_scratch/katana/exams/from_httpx_vcof_sparse.jsonl -depth 3 -c 5 -timeout 15 -fs fqdn -ct 3m` |
| `SCAN_CRAWL_PROFILE` | `depth-3,fqdn-scope,concurrency-5,timeout-15,crawl-duration-3m` |
| `SCAN_ELAPSED` | `705.719` |
| `SCAN_EXIT_STATUS` | `124` |
| `SCAN_RECORD` | `katana:venturecapitalopportunitiesfund.com.au:katana -list .docs/docs-for-cli-tools/exploration_scratch/katana/urls/from_httpx_vcof_sparse_urls.txt -silent -jsonl -o .docs/docs-for-cli-tools/exploration_scratch/katana/exams/from_httpx_vcof_sparse.jsonl -depth 3 -c 5 -timeout 15 -fs fqdn -ct 3m` |
| `SCAN_START` | `2026-07-06T11:25:46.218632+00:00` |
| `SCAN_TARGET` | `venturecapitalopportunitiesfund.com.au` |
| `SCAN_TOOL` | `katana` |
| `SCAN_URL_INPUT_COUNT` | `1` |
| `UPSTREAM_SCENARIO_ID` | `from_subfinder_vcof_sparse` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_CRAWL_PROFILE` |
| `SCAN_RECORD` | `had` | `SCAN_URL_INPUT_COUNT` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `DOMAIN_NAME` |
| `SCAN_RECORD` | `had` | `UPSTREAM_SCENARIO_ID` |
---

*OS-Intel Scan*
