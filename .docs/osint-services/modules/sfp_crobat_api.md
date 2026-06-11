# Crobat API

**Module ID:** `sfp_crobat_api`

## Summary

Search Crobat API for subdomains.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://sonar.omnisint.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `delay` — Delay between requests, in seconds.
- `max_pages` — Maximum number of pages of results to fetch.
- `verify` — DNS resolve each identified subdomain.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=error_failed; Finalize: benign input clean_miss (negative fixture)
