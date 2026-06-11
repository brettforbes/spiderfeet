# CommonCrawl

**Module ID:** `sfp_commoncrawl`

## Summary

Searches for URLs found through CommonCrawl.org.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** http://commoncrawl.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://commoncrawl.org/the-data/get-started/, https://commoncrawl.org/the-data/examples/, https://commoncrawl.org/the-data/tutorials/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `LINKED_URL_INTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Passive

## Module options

- `indexes` — Number of most recent indexes to attempt, because results tend to be occasionally patchy.

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: CommonCrawl index list HTML changed; module cannot parse latest indexes

## Catalogue notes

We build and maintain an open repository of web crawl data that can be accessed and analyzed by anyone.
Everyone should have the opportunity to indulge their curiosities, analyze the world and pursue brilliant ideas. Small startups or even individuals can now access high quality crawl data that was previously only available to large search engine corporations.
