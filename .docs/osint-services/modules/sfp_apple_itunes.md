# Apple iTunes

**Module ID:** `sfp_apple_itunes`

## Summary

Search Apple iTunes for mobile apps.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://itunes.apple.com/
- **Model:** `FREE_AUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `APPSTORE_ENTRY`
- `INTERNET_NAME`
- `LINKED_URL_INTERNAL`
- `AFFILIATE_INTERNET_NAME`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Catalogue notes

The Apple iTunes store is a store for downloading and purchasing apps for Apple devices.
