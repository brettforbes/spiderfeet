# Httpx scan narrative — `from_subfinder_vcof_sparse`

## Introduction

Httpx confirms live web endpoints, HTTP metadata, and technology signals for each probed host under the 10 H0-H7 ruleset.

## Systems

- `HOST` `2606:4700:20::681a:623`

## Relation notes

Seed-defined dns-resolves-to, cname-alias-to, and derived-from relations are represented with approved SPEC-004 relations in this slice until relation coverage is updated.


## Appendix

### Nodes

- `APPLICATIONS`: APPLICATIONS
- `CONTENT_LENGTH`: 23244
- `CONTENT_TYPE`: text/html
- `DOMAIN_NAME`: venturecapitalopportunitiesfund.com.au
- `DOMAIN_NAME`: www.venturecapitalopportunitiesfund.com.au
- `HOST`: 2606:4700:20::681a:623
- `HTTP_LIVENESS_STATUS`: confirmed
- `HTTP_LIVENESS_STATUS`: unconfirmed
- `HTTP_METHOD`: GET
- `HTTP_PATH`: /
- `HTTP_STATUS_CODE`: 200
- `HTTP_TITLE`: Home - Venture Capital Opportunities Fund
- `IPV6_ADDRESS`: 2606:4700:20::681a:623
- `IP_ADDRESS`: 104.26.6.35
- `IP_ADDRESS`: 104.26.7.35
- `IP_ADDRESS`: 172.67.68.161
- `LINE_COUNT`: 298
- `NETWORKS`: NETWORKS
- `PAGE_HASH`: 0
- `PAGE_TYPE`: other
- `PORT`: 443
- `PORT_STATE`: open
- `PROBE_CONNECTED`: false
- `PROBE_FAILED`: False
- `PROBE_TIMESTAMP`: 2026-07-06T02:05:03.3744974+10:00
- `RESPONSE_TIME_MS`: 249.3053ms
- `SCAN_CLI`: httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_vcof_sparse_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_vcof_sparse.jsonl -silent -threads 5 -timeout 15
- `SCAN_ELAPSED`: 2.375
- `SCAN_EXIT_STATUS`: 0
- `SCAN_HOST_INPUT_COUNT`: 1
- `SCAN_PROBE_PROFILE`: status-code,title,tech-detect,server,cdn,ip
- `SCAN_RECORD`: httpx:venturecapitalopportunitiesfund.com.au:httpx -l .docs/docs-for-cli-tools/exploration_scratch/httpx/hosts/from_subfinder_vcof_sparse_hosts.txt -status-code -title -tech-detect -server -cdn -ip -json -no-stdin -o .docs/docs-for-cli-tools/exploration_scratch/httpx/exams/from_subfinder_vcof_sparse.jsonl -silent -threads 5 -timeout 15
- `SCAN_START`: 2026-07-05T16:05:01.072497+00:00
- `SCAN_TARGET`: venturecapitalopportunitiesfund.com.au
- `SCAN_TOOL`: httpx
- `SERVICE`: https
- `SOFTWARE_USED`: Bootstrap
- `SOFTWARE_USED`: Cloudflare
- `SOFTWARE_USED`: Cloudflare Browser Insights
- `SOFTWARE_USED`: Drupal
- `SOFTWARE_USED`: Google Tag Manager
- `SOFTWARE_USED`: HTTP/3
- `SOFTWARE_USED`: PHP
- `SOFTWARE_USED`: cloudflare
- `SOFTWARE_USED`: jQuery
- `SOFTWARE_USED`: jQuery CDN
- `SOFTWARE_USED`: jsDelivr
- `SOFTWARE_VERSION`: 3.3.5
- `SOFTWARE_VERSION`: 7
- `TRANSPORT`: tcp
- `TRANSPORT_PROTOCOL`: tcp
- `UPSTREAM_SCENARIO_ID`: corporate_vcof_sparse_passive
- `WORD_COUNT`: 1779

### Edges

- `SCAN_RECORD` `had` `SCAN_CLI`
- `SCAN_RECORD` `had` `SCAN_TARGET`
- `SCAN_RECORD` `had` `SCAN_PROBE_PROFILE`
- `SCAN_RECORD` `had` `SCAN_HOST_INPUT_COUNT`
- `SCAN_RECORD` `had` `SCAN_START`
- `SCAN_RECORD` `had` `SCAN_ELAPSED`
- `SCAN_RECORD` `had` `SCAN_EXIT_STATUS`
- `SCAN_RECORD` `had` `SCAN_TOOL`
- `SCAN_RECORD` `contains` `DOMAIN_NAME`
- `SCAN_RECORD` `had` `UPSTREAM_SCENARIO_ID`
- `SCAN_RECORD` `contains` `DOMAIN_NAME`
- `DOMAIN_NAME` `had` `HTTP_LIVENESS_STATUS`
- `SCAN_RECORD` `contains` `HOST`
- `DOMAIN_NAME` `had` `HOST`
- `HOST` `contains` `NETWORKS`
- `NETWORKS` `contains` `IPV6_ADDRESS`
- `IPV6_ADDRESS` `contains` `TRANSPORT`
- `TRANSPORT` `had` `TRANSPORT_PROTOCOL`
- `TRANSPORT` `contains` `PORT`
- `PORT` `had` `PORT_STATE`
- `HOST` `contains` `APPLICATIONS`
- `APPLICATIONS` `contains` `SERVICE`
- `SERVICE` `listens-to` `PORT`
- `SERVICE` `had` `HTTP_STATUS_CODE`
- `SERVICE` `had` `HTTP_TITLE`
- `SERVICE` `had` `CONTENT_TYPE`
- `SERVICE` `had` `CONTENT_LENGTH`
- `SERVICE` `had` `HTTP_METHOD`
- `SERVICE` `had` `HTTP_PATH`
- `SERVICE` `had` `RESPONSE_TIME_MS`
- `SERVICE` `had` `WORD_COUNT`
- `SERVICE` `had` `LINE_COUNT`
- `SERVICE` `had` `PROBE_FAILED`
- `SERVICE` `had` `PROBE_TIMESTAMP`
- `SERVICE` `had` `PAGE_TYPE`
- `SERVICE` `had` `PAGE_HASH`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SOFTWARE_USED` `had` `SOFTWARE_VERSION`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SOFTWARE_USED` `had` `SOFTWARE_VERSION`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `DOMAIN_NAME` `had` `IP_ADDRESS`
- `IP_ADDRESS` `had` `PROBE_CONNECTED`
- `DOMAIN_NAME` `had` `IP_ADDRESS`
- `IP_ADDRESS` `had` `PROBE_CONNECTED`
- `DOMAIN_NAME` `had` `IP_ADDRESS`
- `IP_ADDRESS` `had` `PROBE_CONNECTED`
- `DOMAIN_NAME` `had` `HTTP_LIVENESS_STATUS`
