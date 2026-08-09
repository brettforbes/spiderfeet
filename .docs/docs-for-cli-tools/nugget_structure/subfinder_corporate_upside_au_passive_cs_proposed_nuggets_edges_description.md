# Subfinder scan narrative — `corporate_upside_au_passive_cs`

## Introduction

Subfinder contributes DNS-focused domain enumeration. Active-mode IP resolution is retained as an IPV4_ADDRESS fact using currently approved SPEC-004 relations; the exact dns-resolves-to relation remains deferred until relation coverage is updated.

## Scan

Every examination has one SCAN_RECORD with scan descriptors linked via had. This scan includes **1** Scan root node(s) (e.g. `subfinder:theupside.com.au:subfinder -d theupside.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_upside_au_passive_cs.jsonl -silent`). Linked structures: `SCAN_CLI`, `SCAN_TARGET`, `SCAN_MODE`, `SCAN_START`, `SCAN_ELAPSED`, `SCAN_EXIT_STATUS`.

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

### Scan descriptors

| Nugget | Value |
| --- | --- |
| `SCAN_RECORD` | `subfinder:theupside.com.au:subfinder -d theupside.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_upside_au_passive_cs.jsonl -silent` |

## Domains

Apex DOMAIN_NAME entities contain subdomain DOMAIN_NAME children; descriptors capture discovery mode, sources, and liveness. This scan includes **27** Domains root node(s) (e.g. `theupside.com.au`, `aws.theupside.com.au`, `www.aws.theupside.com.au`). Linked structures: no child categories.

### Structure overview

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
```

### `DOMAIN_NAME`

```mermaid
flowchart TD
  domain_name_1["DOMAIN_NAME"]
  domain_name_2["DOMAIN_NAME: aws.theupside.com.au"]
  domain_name_1 -->|contains| domain_name_2
  domain_name_3["DOMAIN_NAME: cfjump.theupside.com.au"]
  domain_name_1 -->|contains| domain_name_3
  domain_name_4["DOMAIN_NAME: dev.theupside.com.au"]
  domain_name_1 -->|contains| domain_name_4
  more_5["+24 more"]
  domain_name_1 -->|contains| more_5
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
| `DOMAIN_NAME` | `www.aws.theupside.com.au` |
| `DOMAIN_NAME` | `www.dev.theupside.com.au` |
| `DOMAIN_NAME` | `www.e.theupside.com.au` |
| `DOMAIN_NAME` | `www.email.theupside.com.au` |
| `DOMAIN_NAME` | `www.info.theupside.com.au` |
| `DOMAIN_NAME` | `www.k8s.theupside.com.au` |
| `DOMAIN_NAME` | `www.mail.theupside.com.au` |
| `DOMAIN_NAME` | `www.news.theupside.com.au` |
| `DOMAIN_NAME` | `www.newsletter.theupside.com.au` |
| `DOMAIN_NAME` | `www.spf.theupside.com.au` |
| `DOMAIN_NAME` | `www.test.theupside.com.au` |
| `DOMAIN_NAME` | `www.theupside.com.au` |
| `DOMAIN_NAME` | `www.track.theupside.com.au` |

## Conclusion

See the appendix for the full node and edge inventory.


## Appendix

### Nodes

| Nugget | Value |
| --- | --- |
| `DISCOVERY_MODE` | `passive` |
| `DISCOVERY_SOURCE` | `crtsh` |
| `DISCOVERY_SOURCE` | `hackertarget` |
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
| `DOMAIN_NAME` | `www.aws.theupside.com.au` |
| `DOMAIN_NAME` | `www.dev.theupside.com.au` |
| `DOMAIN_NAME` | `www.e.theupside.com.au` |
| `DOMAIN_NAME` | `www.email.theupside.com.au` |
| `DOMAIN_NAME` | `www.info.theupside.com.au` |
| `DOMAIN_NAME` | `www.k8s.theupside.com.au` |
| `DOMAIN_NAME` | `www.mail.theupside.com.au` |
| `DOMAIN_NAME` | `www.news.theupside.com.au` |
| `DOMAIN_NAME` | `www.newsletter.theupside.com.au` |
| `DOMAIN_NAME` | `www.spf.theupside.com.au` |
| `DOMAIN_NAME` | `www.test.theupside.com.au` |
| `DOMAIN_NAME` | `www.theupside.com.au` |
| `DOMAIN_NAME` | `www.track.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `aws.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `com.au` |
| `DOMAIN_NAME_PARENT` | `dev.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `e.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `email.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `info.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `k8s.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `mail.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `news.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `newsletter.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `spf.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `test.theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `theupside.com.au` |
| `DOMAIN_NAME_PARENT` | `track.theupside.com.au` |
| `LIVENESS_STATUS` | `unconfirmed` |
| `SCAN_CLI` | `subfinder -d theupside.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_upside_au_passive_cs.jsonl -silent` |
| `SCAN_ELAPSED` | `22.735` |
| `SCAN_EXIT_STATUS` | `0` |
| `SCAN_MODE` | `passive` |
| `SCAN_RECORD` | `subfinder:theupside.com.au:subfinder -d theupside.com.au -oJ -cs -o .docs/docs-for-cli-tools/exploration_scratch/subfinder/exams/corporate_upside_au_passive_cs.jsonl -silent` |
| `SCAN_START` | `2026-07-05T14:23:45.538135+00:00` |
| `SCAN_TARGET` | `theupside.com.au` |
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
