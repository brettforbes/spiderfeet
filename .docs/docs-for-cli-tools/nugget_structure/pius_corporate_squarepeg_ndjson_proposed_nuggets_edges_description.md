# Pius scan narrative — `corporate_squarepeg_ndjson`

## Introduction

Organizational attack-surface findings are grouped under the head company, with domains, affiliates, and unresolved research leads emitted per 08 rules.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `pius:Square Peg Capital Pty Ltd:/mnt/c/projects/spiderfeet/.tools/pius run --org "Square Peg Capital Pty Ltd" --domain squarepeg.vc --plugins gleif,wikidata,whois,crt-sh --output ndjson`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_TARGET_ORG`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`.

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

### Scan descriptors

| Nugget | Value |
| --- | --- |
| `SCAN_RECORD` | `pius:Square Peg Capital Pty Ltd:/mnt/c/projects/spiderfeet/.tools/pius run --org "Square Peg Capital Pty Ltd" --domain squarepeg.vc --plugins gleif,wikidata,whois,crt-sh --output ndjson` |

## Organization

Organisation scans root at COMPANY_NAME with category buckets for domains, netblocks, and research leads. This scan includes **1** Organization root node(s) (e.g. `Square Peg Capital Pty Ltd`). Linked structures: `DOMAINS`.

### Structure overview

```mermaid
flowchart TD
  company_name_1["COMPANY_NAME"]
  domains_2["DOMAINS"]
  company_name_1 -->|contains| domains_2
```

### `DOMAINS`

```mermaid
flowchart TD
  domains_1["DOMAINS"]
  domain_name_2["DOMAIN_NAME: data.squarepeg.vc"]
  domains_1 -->|contains| domain_name_2
  domain_name_3["DOMAIN_NAME: email.foundersummit2026.squarepeg.vc"]
  domains_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: foundersummit2026.squarepeg.vc"]
  domains_1 -->|contains| domain_name_4
  more_5["+3 more"]
  domains_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |

### `NETBLOCKS`

```mermaid
flowchart TD
  netblocks_1["NETBLOCKS"]
  domains_2["DOMAINS: DOMAINS"]
  netblocks_1 -->|contains| domains_2
  domain_name_3["DOMAIN_NAME: data.squarepeg.vc"]
  netblocks_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: email.foundersummit2026.squarepeg.vc"]
  netblocks_1 -->|contains| domain_name_4
  more_5["+4 more"]
  netblocks_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `DOMAINS` | `DOMAINS` |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |

### `LEADS`

```mermaid
flowchart TD
  leads_1["LEADS"]
  domains_2["DOMAINS: DOMAINS"]
  leads_1 -->|contains| domains_2
  domain_name_3["DOMAIN_NAME: data.squarepeg.vc"]
  leads_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: email.foundersummit2026.squarepeg.vc"]
  leads_1 -->|contains| domain_name_4
  more_5["+4 more"]
  leads_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `DOMAINS` | `DOMAINS` |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **6** Domains root node(s) (e.g. `www.squarepeg.vc`, `squarepeg.vc`, `foundersummit2026.squarepeg.vc`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### `DOMAIN_NAME`

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
  domain_name_2["DOMAIN_NAME: data.squarepeg.vc"]
  domain_name_1 -->|contains| domain_name_2
  domain_name_3["DOMAIN_NAME: email.foundersummit2026.squarepeg.vc"]
  domain_name_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: foundersummit2026.squarepeg.vc"]
  domain_name_1 -->|contains| domain_name_4
  more_5["+3 more"]
  domain_name_1 -->|contains| more_5
```

| Nugget | Value |
| --- | --- |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `COMPANY_NAME` | `Square Peg Capital Pty Ltd` |
| `DISCOVERY_METHOD` | `certificate-transparency` |
| `DOMAINS` | `DOMAINS` |
| `DOMAIN_NAME` | `data.squarepeg.vc` |
| `DOMAIN_NAME` | `email.foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME` | `helix.squarepeg.vc` |
| `DOMAIN_NAME` | `squarepeg.vc` |
| `DOMAIN_NAME` | `www.squarepeg.vc` |
| `DOMAIN_NAME_PARENT` | `foundersummit2026.squarepeg.vc` |
| `DOMAIN_NAME_PARENT` | `squarepeg.vc` |
| `REVIEW_STATUS` | `confirmed` |
| `SCAN_CLI` | `/mnt/c/projects/spiderfeet/.tools/pius run --org "Square Peg Capital Pty Ltd" --domain squarepeg.vc --plugins gleif,wikidata,whois,crt-sh --output ndjson` |
| `SCAN_ELAPSED` | `35.046` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_RECORD` | `pius:Square Peg Capital Pty Ltd:/mnt/c/projects/spiderfeet/.tools/pius run --org "Square Peg Capital Pty Ltd" --domain squarepeg.vc --plugins gleif,wikidata,whois,crt-sh --output ndjson` |
| `SCAN_START` | `2026-07-05T13:10:18.904973+00:00` |
| `SCAN_TARGET` | `squarepeg.vc` |
| `SCAN_TARGET_ORG` | `Square Peg Capital Pty Ltd` |
| `SCAN_TOOL` | `pius` |

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
| `DOMAIN_NAME` | `had` | `DISCOVERY_METHOD` |
| `DOMAIN_NAME` | `had` | `DOMAIN_NAME_PARENT` |
| `COMPANY_NAME` | `contains` | `DOMAINS` |
| `DOMAINS` | `contains` | `DOMAIN_NAME` |
| `COMPANY_NAME` | `contains` | `DOMAIN_NAME` |
| `DOMAIN_NAME` | `had` | `REVIEW_STATUS` |
---

*OS-Intel Scan*
