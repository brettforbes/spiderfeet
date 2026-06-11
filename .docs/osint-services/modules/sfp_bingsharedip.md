# Bing (Shared IPs)

**Module ID:** `sfp_bingsharedip`

## Summary

Search Bing for hosts sharing the same IP.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.bing.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `CO_HOSTED_SITE`
- `IP_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Bing API Key for shared IP search.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `pages` — Number of max bing results to request from API.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

The Bing Search APIs let you build web-connected apps and services that find webpages, images, news, locations, and more without advertisements.
