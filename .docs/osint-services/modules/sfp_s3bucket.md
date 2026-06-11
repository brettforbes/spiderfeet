# Amazon S3 Bucket Finder

**Module ID:** `sfp_s3bucket`

## Summary

Search for potential Amazon S3 buckets associated with the target and attempt to list their contents.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** https://aws.amazon.com/s3/
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
- `endpoints` — Different S3 endpoints to check where buckets may exist, as per http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
- `suffixes` — List of suffixes to append to domains tried as bucket names

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: S3 bucket brute-force exceeds practical scan_ui timeout; defer to module-tuning issue

## Catalogue notes

Amazon S3 is cloud object storage with industry-leading scalability, data availability, security, and performance. S3 is ideal for data lakes, mobile applications, backup and restore, archival, IoT devices, ML, AI, and analytics.
