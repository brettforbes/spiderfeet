# Google Object Storage Finder

**Module ID:** `sfp_googleobjectstorage`

## Summary

Search for potential Google Object Storage buckets associated with the target and attempt to list their contents.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://cloud.google.com/storage
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `LINKED_URL_EXTERNAL`
- **Produced:**
- `CLOUD_STORAGE_BUCKET`
- `CLOUD_STORAGE_BUCKET_OPEN`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Passive

## Module options

- `_maxthreads` — Maximum threads
- `suffixes` — List of suffixes to append to domains tried as bucket names

## Test seeds

- `DOMAIN_NAME`: input=`youtube.com` validation=smoke status=FINISHED; verdict=hit; Per-module research probe; status=FINISHED

## Catalogue notes

Object storage for companies of all sizes.Secure, durable, and with low latency. Store any amount of data.Retrieve it as often as you'd like.
