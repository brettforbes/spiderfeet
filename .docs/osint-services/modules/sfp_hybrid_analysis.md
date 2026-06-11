# Hybrid Analysis

**Module ID:** `sfp_hybrid_analysis`

## Summary

Search Hybrid Analysis for domains and URLs related to the target.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.hybrid-analysis.com
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://www.hybrid-analysis.com/knowledge-base, https://www.hybrid-analysis.com/docs/api/v2

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `LINKED_URL_INTERNAL`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Hybrid Analysis API key.
- `delay` — Delay between requests, in seconds.
- `verify` — Verify identified domains still resolve to the associated specified IP address.

## Catalogue notes

A free malware analysis service for the community. Using this service you can submit files for in-depth static and dynamic analysis.
