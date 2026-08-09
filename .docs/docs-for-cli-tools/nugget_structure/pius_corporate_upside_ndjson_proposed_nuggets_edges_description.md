# Pius scan narrative — `corporate_upside_ndjson`

## Introduction

Organizational attack-surface findings are grouped under the head company, with domains, affiliates, and unresolved research leads emitted per 08 rules.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `pius:The Upside Pty Ltd:/mnt/c/projects/spiderfeet/.tools/pius run --org "The Upside Pty Ltd" --domain theupside.com.au --plugins gleif,wikidata,whois,crt-sh --output ndjson`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_TARGET_ORG`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`.

### Structure overview

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_cli_2["SCAN_CLI"]
  scan_record_1 -->|had| scan_cli_2
  scan_target_3["SCAN_TARGET"]
  scan_record_1 -->|had| scan_target_3
  scan_target_org_4["SCAN_TARGET_ORG"]
  scan_record_1 -->|had| scan_target_org_4
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
  scan_cli_2["SCAN_CLI: /mnt/c/projects/spiderfeet/.tools/pius …"]
  scan_record_1 -->|contains| scan_cli_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_CLI` | `/mnt/c/projects/spiderfeet/.tools/pius run --org "The Upside Pty Ltd" --domain theupside.com.au --plugins gleif,wikidata,whois,crt-sh --output ndjson` |

### `SCAN_TARGET`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_2["SCAN_TARGET: theupside.com.au"]
  scan_record_1 -->|contains| scan_target_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET` | `theupside.com.au` |

### `SCAN_TARGET_ORG`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_target_org_2["SCAN_TARGET_ORG: The Upside Pty Ltd"]
  scan_record_1 -->|contains| scan_target_org_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TARGET_ORG` | `The Upside Pty Ltd` |

### `SCAN_START`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_start_2["SCAN_START: 2026-07-05T13:10:54.341348+00:00"]
  scan_record_1 -->|contains| scan_start_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_START` | `2026-07-05T13:10:54.341348+00:00` |

### `SCAN_ELAPSED`

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  scan_elapsed_2["SCAN_ELAPSED: 16.125"]
  scan_record_1 -->|contains| scan_elapsed_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_ELAPSED` | `16.125` |

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
  scan_tool_2["SCAN_TOOL: pius"]
  scan_record_1 -->|contains| scan_tool_2
```

| Nugget | Value |
| --- | --- |
| `SCAN_TOOL` | `pius` |

## Organization

Organisation scans root at COMPANY_NAME with category buckets for domains, netblocks, and research leads. This scan includes **1** Organization root node(s) (e.g. `The Upside Pty Ltd`). Linked structures: `LEADS`, `DOMAINS`.

### Structure overview

```mermaid
flowchart TD
  company_name_1["COMPANY_NAME"]
  leads_2["LEADS"]
  company_name_1 -->|contains| leads_2
  domains_3["DOMAINS"]
  company_name_1 -->|contains| domains_3
```

### `LEADS`

```mermaid
flowchart TD
  leads_1["LEADS"]
  candidate_entity_2["CANDIDATE_ENTITY: CEO"]
  leads_1 -->|contains| candidate_entity_2
```

| Nugget | Value |
| --- | --- |
| `CANDIDATE_ENTITY` | `CEO` |

### `DOMAINS`

```mermaid
flowchart TD
  domains_1["DOMAINS"]
  domain_name_2["DOMAIN_NAME: aws.theupside.com.au"]
  domains_1 -->|contains| domain_name_2
  domain_name_3["DOMAIN_NAME: cfjump.theupside.com.au"]
  domains_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: dev.theupside.com.au"]
  domains_1 -->|contains| domain_name_4
  more_5["+12 more"]
  domains_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `aws.theupside.com.au` |
| `DOMAIN_NAME` | `cfjump.theupside.com.au` |
| `DOMAIN_NAME` | `dev.theupside.com.au` |
| `DOMAIN_NAME` | `e.theupside.com.au` |
| `DOMAIN_NAME` | `email.theupside.com.au` |
| `DOMAIN_NAME` | `info.theupside.com.au` |
| `DOMAIN_NAME` | `k8s.theupside.com.au` |
| `DOMAIN_NAME` | `mail.theupside.com.au` |
| `DOMAIN_NAME` | `news.theupside.com.au` |
| `DOMAIN_NAME` | `newsletter.theupside.com.au` |
| `DOMAIN_NAME` | `spf.theupside.com.au` |
| `DOMAIN_NAME` | `test.theupside.com.au` |
| `DOMAIN_NAME` | `theupside.com.au` |
| `DOMAIN_NAME` | `track.theupside.com.au` |
| `DOMAIN_NAME` | `www.theupside.com.au` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **15** Domains root node(s) (e.g. `theupside.com.au`, `www.theupside.com.au`, `track.theupside.com.au`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### Values

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `aws.theupside.com.au` |
| `DOMAIN_NAME` | `cfjump.theupside.com.au` |
| `DOMAIN_NAME` | `dev.theupside.com.au` |
| `DOMAIN_NAME` | `e.theupside.com.au` |
| `DOMAIN_NAME` | `email.theupside.com.au` |
| `DOMAIN_NAME` | `info.theupside.com.au` |
| `DOMAIN_NAME` | `k8s.theupside.com.au` |
| `DOMAIN_NAME` | `mail.theupside.com.au` |
| `DOMAIN_NAME` | `news.theupside.com.au` |
| `DOMAIN_NAME` | `newsletter.theupside.com.au` |
| `DOMAIN_NAME` | `spf.theupside.com.au` |
| `DOMAIN_NAME` | `test.theupside.com.au` |
| `DOMAIN_NAME` | `theupside.com.au` |
| `DOMAIN_NAME` | `track.theupside.com.au` |
| `DOMAIN_NAME` | `www.theupside.com.au` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `CANDIDATE_ENTITY` | `CEO` |
| `COMPANY_NAME` | `The Upside Pty Ltd` |
| `DISCOVERY_METHOD` | `certificate-transparency` |
| `DOMAINS` | `DOMAINS` |
| `DOMAIN_NAME` | `aws.theupside.com.au` |
| `DOMAIN_NAME` | `cfjump.theupside.com.au` |
| `DOMAIN_NAME` | `dev.theupside.com.au` |
| `DOMAIN_NAME` | `e.theupside.com.au` |
| `DOMAIN_NAME` | `email.theupside.com.au` |
| `DOMAIN_NAME` | `info.theupside.com.au` |
| `DOMAIN_NAME` | `k8s.theupside.com.au` |
| `DOMAIN_NAME` | `mail.theupside.com.au` |
| `DOMAIN_NAME` | `news.theupside.com.au` |
| `DOMAIN_NAME` | `newsletter.theupside.com.au` |
| `DOMAIN_NAME` | `spf.theupside.com.au` |
| `DOMAIN_NAME` | `test.theupside.com.au` |
| `DOMAIN_NAME` | `theupside.com.au` |
| `DOMAIN_NAME` | `track.theupside.com.au` |
| `DOMAIN_NAME` | `www.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `com.au` |
| `DOMAIN_NAME_PARENT` | `theupside.com.au` |
| `DOMAIN_REGISTRAR` | `.au Domain Administration Limited` |
| `IS_PLACEHOLDER` | `true` |
| `IS_WILDCARD_DNS` | `true` |
| `LEADS` | `LEADS` |
| `NEEDS_REVIEW` | `true` |
| `PRESEED_TYPE` | `whois+name` |
| `REVIEW_STATUS` | `confirmed` |
| `SCAN_CLI` | `/mnt/c/projects/spiderfeet/.tools/pius run --org "The Upside Pty Ltd" --domain theupside.com.au --plugins gleif,wikidata,whois,crt-sh --output ndjson` |
| `SCAN_ELAPSED` | `16.125` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_RECORD` | `pius:The Upside Pty Ltd:/mnt/c/projects/spiderfeet/.tools/pius run --org "The Upside Pty Ltd" --domain theupside.com.au --plugins gleif,wikidata,whois,crt-sh --output ndjson` |
| `SCAN_START` | `2026-07-05T13:10:54.341348+00:00` |
| `SCAN_TARGET` | `theupside.com.au` |
| `SCAN_TARGET_ORG` | `The Upside Pty Ltd` |
| `SCAN_TOOL` | `pius` |
| `SUBDOMAIN_ENUMERATION_SUPPRESSED` | `true` |
| `WILDCARD_IP_COUNT` | `1` |

### Edges

| Source | Relation | Target |
| --- | --- | --- |
| `SCAN_RECORD` | `had` | `SCAN_CLI` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET` |
| `SCAN_RECORD` | `had` | `SCAN_TARGET_ORG` |
| `SCAN_RECORD` | `had` | `SCAN_START` |
| `SCAN_RECORD` | `had` | `SCAN_ELAPSED` |
| `SCAN_RECORD` | `had` | `SCAN_EXIT_STATUS` |
| `SCAN_RECORD` | `had` | `SCAN_TOOL` |
| `SCAN_RECORD` | `contains` | `COMPANY_NAME` |
| `COMPANY_NAME` | `contains` | `DOMAIN_REGISTRAR` |
| `CANDIDATE_ENTITY` | `had` | `PRESEED_TYPE` |
| `CANDIDATE_ENTITY` | `had` | `IS_PLACEHOLDER` |
| `CANDIDATE_ENTITY` | `had` | `NEEDS_REVIEW` |
| `COMPANY_NAME` | `contains` | `LEADS` |
| `LEADS` | `contains` | `CANDIDATE_ENTITY` |
| `COMPANY_NAME` | `contains` | `CANDIDATE_ENTITY` |
| `CANDIDATE_ENTITY` | `had` | `REVIEW_STATUS` |
| `DOMAIN_NAME` | `had` | `DISCOVERY_METHOD` |
| `DOMAIN_NAME` | `had` | `DOMAIN_NAME_PARENT` |
| `COMPANY_NAME` | `contains` | `DOMAINS` |
| `DOMAINS` | `contains` | `DOMAIN_NAME` |
| `COMPANY_NAME` | `contains` | `DOMAIN_NAME` |
| `DOMAIN_NAME` | `had` | `REVIEW_STATUS` |
| `DOMAIN_NAME` | `had` | `IS_WILDCARD_DNS` |
| `DOMAIN_NAME` | `had` | `WILDCARD_IP_COUNT` |
| `DOMAIN_NAME` | `had` | `SUBDOMAIN_ENUMERATION_SUPPRESSED` |
---

*OS-Intel Scan*
