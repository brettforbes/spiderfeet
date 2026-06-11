# Azure Blob Finder

**Module ID:** `sfp_azureblobstorage`

## Summary

Search for potential Azure blobs associated with the target and attempt to list their contents.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://azure.microsoft.com/en-in/services/storage/blobs/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `LINKED_URL_EXTERNAL`
- **Produced:**
- `CLOUD_STORAGE_BUCKET`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Passive

## Module options

- `_maxthreads` — Maximum threads
- `suffixes` — List of suffixes to append to domains tried as blob storage names

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

Massively scalable and secure object storage for cloud-native workloads,archives, data lakes, high-performance computing and machine learning.
