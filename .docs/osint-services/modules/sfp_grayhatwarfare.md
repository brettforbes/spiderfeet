# Grayhat Warfare

**Module ID:** `sfp_grayhatwarfare`

## Summary

Find bucket names matching the keyword extracted from a domain from Grayhat API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://buckets.grayhatwarfare.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://buckets.grayhatwarfare.com/docs/api/v1

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `CLOUD_STORAGE_BUCKET`
- `CLOUD_STORAGE_BUCKET_OPEN`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Grayhat Warfare API key.
- `max_pages` — Maximum number of pages to fetch.
- `pause` — Number of seconds to wait between each API call.
- `per_page` — Maximum number of results per page (Max: 1000).

## Catalogue notes

It is a searchable database of open buckets.Has up to million results of each bucket.Full text search with binary logic (can search for keywords and also stopwords)
