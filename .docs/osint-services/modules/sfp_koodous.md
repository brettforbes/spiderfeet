# Koodous

**Module ID:** `sfp_koodous`

## Summary

Search Koodous for mobile apps.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://koodous.com/apks/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.koodous.com/api/apks.html, https://docs.koodous.com/apks.html#apks-search-system

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `APPSTORE_ENTRY`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Module options

- `api_key` — Koodous API key.
- `max_pages` — Maximum number of pages of results to fetch.
