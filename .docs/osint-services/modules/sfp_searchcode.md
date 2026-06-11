# searchcode

**Module ID:** `sfp_searchcode`

## Summary

Search searchcode for code repositories mentioning the target domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** https://searchcode.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://searchcode.com/api/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `LINKED_URL_INTERNAL`
- `PUBLIC_CODE_REPO`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Module options

- `dns_resolve` — DNS resolve each identified domain.
- `max_pages` — Maximum number of pages of results to fetch.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: searchcode.com API returns HTTP 404
