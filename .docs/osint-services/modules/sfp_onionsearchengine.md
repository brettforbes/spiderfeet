# Onionsearchengine.com

**Module ID:** `sfp_onionsearchengine`

## Summary

Search Tor onionsearchengine.com for mentions of the target domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://as.onionsearchengine.com
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://helpdesk.onionsearchengine.com/?v=knowledgebase, https://onionsearchengine.com/add_url.php

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `HUMAN_NAME`
- `EMAILADDR`
- **Produced:**
- `DARKNET_MENTION_URL`
- `DARKNET_MENTION_CONTENT`

## Flags and categories

- **Flags:** tor
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate

## Module options

- `blacklist` — Exclude results from sites matching these patterns.
- `fetchlinks` — Fetch the darknet pages (via TOR, if enabled) to verify they mention your target.
- `fullnames` — Search for human names?
- `max_pages` — Maximum number of pages of results to fetch.
- `timeout` — Query timeout, in seconds.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

No cookies, no javascript, no trace. We protect your privacy.
Onion search engine is search engine with ability to find content on tor network / deepweb / darkweb.
