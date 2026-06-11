# Bing

**Module ID:** `sfp_bingsearch`

## Summary

Obtain information from bing to identify sub-domains and links.

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

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `LINKED_URL_INTERNAL`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Bing API Key for Bing search.
- `pages` — Number of max bing results to request from the API.

## Catalogue notes

The Bing Search APIs let you build web-connected apps and services that find webpages, images, news, locations, and more without advertisements.
