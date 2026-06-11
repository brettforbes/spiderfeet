# DuckDuckGo

**Module ID:** `sfp_duckduckgo`

## Summary

Query DuckDuckGo's API for descriptive information about your target.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://duckduckgo.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://api.duckduckgo.com/api, https://help.duckduckgo.com/company/partnerships/, https://help.duckduckgo.com/duckduckgo-help-pages/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `DOMAIN_NAME_PARENT`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- **Produced:**
- `DESCRIPTION_CATEGORY`
- `DESCRIPTION_ABSTRACT`
- `AFFILIATE_DESCRIPTION_CATEGORY`
- `AFFILIATE_DESCRIPTION_ABSTRACT`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `affiliatedomains` — For affiliates, look up the domain name, not the hostname. This will usually return more meaningful information about the affiliate.

## Test seeds

- `AFFILIATE_INTERNET_NAME`: input=`bbc.co.uk` validation=smoke smoke
- `DOMAIN_NAME`: input=`bbc.co.uk` validation=smoke status=FINISHED; verdict=hit
- `DOMAIN_NAME_PARENT`: input=`co.uk` validation=pilot pilot
- `INTERNET_NAME`: input=`bbc.co.uk` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

Our Instant Answer API gives you free access to many of our instant answers like: topic summaries , categories, disambiguation, and !bang redirects.
