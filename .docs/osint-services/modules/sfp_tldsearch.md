# TLD Searcher

**Module ID:** `sfp_tldsearch`

## Summary

Search all Internet TLDs for domains with the same name as the target (this can be very slow.)

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tldsearch
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tldsearch

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `SIMILARDOMAIN`

## Flags and categories

- **Flags:** slow
- **Categories:** DNS
- **Use cases:** Footprint

## Module options

- `_maxthreads` — Maximum threads
- `activeonly` — Only report domains that have content (try to fetch the page)?
- `skipwildcards` — Skip TLDs and sub-TLDs that have wildcard DNS.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=3

## Catalogue notes

Search all Internet TLDs for domains with the same name as the target (this can be very slow.)

**Module ID:** `sfp_tldsearch`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME
**Produces:** SIMILARDOMAIN
**Flags:** slow

**Smoke battery:**
- Classification: `timeout`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 0
