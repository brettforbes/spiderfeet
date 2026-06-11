# Digital Ocean Space Finder

**Module ID:** `sfp_digitaloceanspace`

## Summary

Search for potential Digital Ocean Spaces associated with the target and attempt to list their contents.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.digitalocean.com/products/spaces/
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
- `endpoints` — Different Digital Ocean locations to check where spaces may exist.
- `suffixes` — List of suffixes to append to domains tried as space names

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

Store and deliver vast amounts of content.S3-compatible object storage with a built-in CDN that makes scaling easy, reliable, and affordable.
