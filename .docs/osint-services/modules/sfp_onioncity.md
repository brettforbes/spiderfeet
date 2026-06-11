# Onion.link

**Module ID:** `sfp_onioncity`

## Summary

Search Tor 'Onion City' search engine for mentions of the target domain using Google Custom Search.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://onion.link/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://developers.google.com/custom-search/v1, https://developers.google.com/custom-search/docs/overview, https://cse.google.com/cse

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- **Produced:**
- `DARKNET_MENTION_URL`
- `DARKNET_MENTION_CONTENT`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey, tor
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate

## Module options

- `api_key` — Google API Key for Onion.link search.
- `cse_id` — Google Custom Search Engine ID.
- `fetchlinks` — Fetch the darknet pages (via TOR, if enabled) to verify they mention your target.
- `fullnames` — Search for human names?
