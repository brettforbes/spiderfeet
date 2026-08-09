# Httpx scan narrative — `from_subfinder_k2am_passive`

## Introduction

Httpx confirms live web endpoints, HTTP metadata, and technology signals for each probed host under the 10 H0-H7 ruleset.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `httpx:k2am.com.au:httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_k2am_passive_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_k2am_passive.jsonl -silent -threads 15 -timeout 15 -rate-limit 30`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_PROBE_PROFILE`, `SCAN_HOST_INPUT_COUNT`, `SCAN_START`, `SCAN_ELAPSED`.

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
| `SCAN_CLI` | `httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_k2am_passive_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_k2am_passive.jsonl -silent -threads 15 -timeout 15 -rate-limit 30` |

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
  scan_host_input_count_2["SCAN_HOST_INPUT_COUNT: 18"]
  scan_record_1 -->|contains| scan_host_input_count_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_HOST_INPUT_COUNT` | `18` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-07-05T16:05:03.491676+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-05T16:05:03.491676+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 21.782"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `21.782` |

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
  upstream_scenario_id_2["UPSTREAM_SCENARIO_ID: corporate_k2am_passive_cs"]
  scan_record_1 -->|contains| upstream_scenario_id_2
```

| Nugget | Value |
| --- | --- |
| `UPSTREAM_SCENARIO_ID` | `corporate_k2am_passive_cs` |

## Host

Qualified HOST endpoints own category trees for networks, applications, environment, and security findings. This scan includes **2** Host root node(s) (e.g. `101.0.68.158`, `170.187.131.209`). Linked structures: `NETWORKS`, `APPLICATIONS`.

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
  ipv4_address_2["IPV4_ADDRESS: 101.0.68.158"]
  networks_1 -->|contains| ipv4_address_2
  ipv4_address_3["IPV4_ADDRESS: 104.18.34.21"]
  networks_1 -->|contains| ipv4_address_3
  ipv4_address_4["IPV4_ADDRESS: 172.64.153.235"]
  networks_1 -->|contains| ipv4_address_4
  more_5["+1 more"]
  networks_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `101.0.68.158` |
| `IPV4_ADDRESS` | `104.18.34.21` |
| `IPV4_ADDRESS` | `172.64.153.235` |
| `IPV4_ADDRESS` | `185.3.93.228` |

### `APPLICATIONS`

```mermaid
flowchart TD
  applications_1["APPLICATIONS"]
  service_2["SERVICE: http"]
  applications_1 -->|contains| service_2
  service_3["SERVICE: https"]
  applications_1 -->|contains| service_3
```

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http` |
| `SERVICE` | `https` |

## CDN

CDN edge endpoints replace HOST when fronting is detected; origin host count may be indeterminate. This scan includes **1** CDN root node(s) (e.g. `104.18.34.21`). Linked structures: `NETWORKS`, `APPLICATIONS`.

### Structure overview

```mermaid
flowchart TD
  cdn_1["CDN"]
  networks_2["NETWORKS"]
  cdn_1 -->|contains| networks_2
  applications_3["APPLICATIONS"]
  cdn_1 -->|contains| applications_3
```

### `NETWORKS`

```mermaid
flowchart TD
  networks_1["NETWORKS"]
  ipv4_address_2["IPV4_ADDRESS: 101.0.68.158"]
  networks_1 -->|contains| ipv4_address_2
  ipv4_address_3["IPV4_ADDRESS: 104.18.34.21"]
  networks_1 -->|contains| ipv4_address_3
  ipv4_address_4["IPV4_ADDRESS: 172.64.153.235"]
  networks_1 -->|contains| ipv4_address_4
  more_5["+1 more"]
  networks_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `IPV4_ADDRESS` | `101.0.68.158` |
| `IPV4_ADDRESS` | `104.18.34.21` |
| `IPV4_ADDRESS` | `172.64.153.235` |
| `IPV4_ADDRESS` | `185.3.93.228` |

### `APPLICATIONS`

```mermaid
flowchart TD
  applications_1["APPLICATIONS"]
  service_2["SERVICE: http"]
  applications_1 -->|contains| service_2
  service_3["SERVICE: https"]
  applications_1 -->|contains| service_3
```

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http` |
| `SERVICE` | `https` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **7** Domains root node(s) (e.g. `k2am.com.au`, `ksm.k2am.com.au`, `unbouncepages.com`). Linked structures: `DOMAIN_NAME`.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
  domain_name_2["DOMAIN_NAME subdomain"]
  domain_name_1 -->|contains| domain_name_2
```

### `DOMAIN_NAME`

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
  domain_name_2["DOMAIN_NAME: track.smtp2go.net"]
  domain_name_1 -->|contains| domain_name_2
  domain_name_3["DOMAIN_NAME: unbouncepages.com"]
  domain_name_1 -->|contains| domain_name_3
```

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `track.smtp2go.net` |
| `DOMAIN_NAME` | `unbouncepages.com` |

## Services and ports

APPLICATION services listen-to PORT entities under NETWORKS/TRANSPORT. This scan includes **2** Services and ports root node(s) (e.g. `http`, `https`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  service_1["SERVICE"]
```

### Values

| Nugget | Value |
| --- | --- |
| `SERVICE` | `http` |
| `SERVICE` | `https` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `APPLICATIONS` | `APPLICATIONS` |
| `CDN` | `104.18.34.21` |
| `CDN_NAME` | `cloudflare` |
| `CDN_TYPE` | `waf` |
| `CNAME_TARGET` | `track.smtp2go.net` |
| `CNAME_TARGET` | `unbouncepages.com` |
| `CONTENT_LENGTH` | `13336` |
| `CONTENT_LENGTH` | `16` |
| `CONTENT_LENGTH` | `2334` |
| `CONTENT_TYPE` | `text/html` |
| `CONTENT_TYPE` | `text/plain` |
| `DOMAIN_NAME` | `k2am.com.au` |
| `DOMAIN_NAME` | `kii.k2am.com.au` |
| `DOMAIN_NAME` | `ksm.k2am.com.au` |
| `DOMAIN_NAME` | `link.k2am.com.au` |
| `DOMAIN_NAME` | `track.smtp2go.net` |
| `DOMAIN_NAME` | `unbouncepages.com` |
| `DOMAIN_NAME` | `www.k2am.com.au` |
| `HOST` | `101.0.68.158` |
| `HOST` | `170.187.131.209` |
| `HTTP_LIVENESS_STATUS` | `confirmed` |
| `HTTP_LIVENESS_STATUS` | `unconfirmed` |
| `HTTP_METHOD` | `GET` |
| `HTTP_PATH` | `/` |
| `HTTP_STATUS_CODE` | `200` |
| `HTTP_STATUS_CODE` | `409` |
| `HTTP_TITLE` | `Home` |
| `HTTP_TITLE` | `SMTP2GO` |
| `IPV4_ADDRESS` | `101.0.68.158` |
| `IPV4_ADDRESS` | `104.18.34.21` |
| `IPV4_ADDRESS` | `170.187.131.209` |
| `IPV4_ADDRESS` | `172.64.153.235` |
| `IPV4_ADDRESS` | `185.3.93.228` |
| `IS_ERROR_PAGE` | `true` |
| `LINE_COUNT` | `1` |
| `LINE_COUNT` | `419` |
| `LINE_COUNT` | `84` |
| `NETWORKS` | `NETWORKS` |
| `PAGE_HASH` | `0` |
| `PAGE_TYPE` | `error` |
| `PAGE_TYPE` | `nonerror` |
| `PORT` | `443` |
| `PORT` | `80` |
| `PORT_STATE` | `open` |
| `PROBE_CONNECTED` | `false` |
| `PROBE_CONNECTED` | `true` |
| `PROBE_FAILED` | `False` |
| `PROBE_TIMESTAMP` | `2026-07-06T02:05:05.3292777+10:00` |
| `PROBE_TIMESTAMP` | `2026-07-06T02:05:05.3361793+10:00` |
| `PROBE_TIMESTAMP` | `2026-07-06T02:05:05.4655046+10:00` |
| `PROBE_TIMESTAMP` | `2026-07-06T02:05:06.2194447+10:00` |
| `RESPONSE_TIME_MS` | `120.6392ms` |
| `RESPONSE_TIME_MS` | `23.1847ms` |
| `RESPONSE_TIME_MS` | `26.6143ms` |
| `RESPONSE_TIME_MS` | `966.9239ms` |
| `SCAN_CLI` | `httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_k2am_passive_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_k2am_passive.jsonl -silent -threads 15 -timeout 15 -rate-limit 30` |
| `SCAN_ELAPSED` | `21.782` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_HOST_INPUT_COUNT` | `18` |
| `SCAN_PROBE_PROFILE` | `status-code,title,tech-detect,server,cdn,ip` |
| `SCAN_RECORD` | `httpx:k2am.com.au:httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_k2am_passive_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_k2am_passive.jsonl -silent -threads 15 -timeout 15 -rate-limit 30` |
| `SCAN_START` | `2026-07-05T16:05:03.491676+00:00` |
| `SCAN_TARGET` | `k2am.com.au` |
| `SCAN_TOOL` | `httpx` |
| `SERVICE` | `http` |
| `SERVICE` | `https` |
| `SOFTWARE_USED` | `Apache` |
| `SOFTWARE_USED` | `Apache HTTP Server` |
| `SOFTWARE_USED` | `Bootstrap` |
| `SOFTWARE_USED` | `Chart.js` |
| `SOFTWARE_USED` | `Cloudflare` |
| `SOFTWARE_USED` | `D3` |
| `SOFTWARE_USED` | `Google Hosted Libraries` |
| `SOFTWARE_USED` | `HSTS` |
| `SOFTWARE_USED` | `Modernizr` |
| `SOFTWARE_USED` | `PHP` |
| `SOFTWARE_USED` | `Slick` |
| `SOFTWARE_USED` | `cdnjs` |
| `SOFTWARE_USED` | `cloudflare` |
| `SOFTWARE_USED` | `jQuery` |
| `SOFTWARE_VERSION` | `2.4.0` |
| `TRANSPORT` | `tcp` |
| `TRANSPORT_PROTOCOL` | `tcp` |
| `UPSTREAM_SCENARIO_ID` | `corporate_k2am_passive_cs` |
| `WORD_COUNT` | `1070` |
| `WORD_COUNT` | `3` |
| `WORD_COUNT` | `642` |

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
| `SCAN_RECORD` | `contains` | `CDN` |
| `DOMAIN_NAME` | `had` | `CDN` |
| `CDN` | `had` | `CDN_NAME` |
| `CDN` | `had` | `CDN_TYPE` |
| `CDN` | `contains` | `NETWORKS` |
| `NETWORKS` | `contains` | `IPV4_ADDRESS` |
| `IPV4_ADDRESS` | `contains` | `TRANSPORT` |
| `TRANSPORT` | `had` | `TRANSPORT_PROTOCOL` |
| `TRANSPORT` | `contains` | `PORT` |
| `PORT` | `had` | `PORT_STATE` |
| `CDN` | `contains` | `APPLICATIONS` |
| `APPLICATIONS` | `contains` | `SERVICE` |
| `SERVICE` | `listens-to` | `PORT` |
| `SERVICE` | `had` | `HTTP_STATUS_CODE` |
| `SERVICE` | `had` | `CONTENT_TYPE` |
| `SERVICE` | `had` | `CONTENT_LENGTH` |
| `SERVICE` | `had` | `HTTP_METHOD` |
| `SERVICE` | `had` | `HTTP_PATH` |
| `SERVICE` | `had` | `RESPONSE_TIME_MS` |
| `SERVICE` | `had` | `WORD_COUNT` |
| `SERVICE` | `had` | `LINE_COUNT` |
| `SERVICE` | `had` | `PROBE_FAILED` |
| `SERVICE` | `had` | `PROBE_TIMESTAMP` |
| `SERVICE` | `had` | `PAGE_TYPE` |
| `SERVICE` | `had` | `PAGE_HASH` |
| `SERVICE` | `had` | `IS_ERROR_PAGE` |
| `SERVICE` | `contains` | `SOFTWARE_USED` |
| `DOMAIN_NAME` | `had` | `DOMAIN_NAME` |
| `DOMAIN_NAME` | `had` | `CNAME_TARGET` |
| `DOMAIN_NAME` | `had` | `IPV4_ADDRESS` |
| `IPV4_ADDRESS` | `had` | `PROBE_CONNECTED` |
| `SCAN_RECORD` | `contains` | `HOST` |
| `DOMAIN_NAME` | `had` | `HOST` |
| `HOST` | `contains` | `NETWORKS` |
| `HOST` | `contains` | `APPLICATIONS` |
| `SERVICE` | `had` | `HTTP_TITLE` |
| `SOFTWARE_USED` | `had` | `SOFTWARE_VERSION` |
---

*OS-Intel Scan*
