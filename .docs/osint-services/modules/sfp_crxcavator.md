# CRXcavator

**Module ID:** `sfp_crxcavator`

## Summary

Search CRXcavator for Chrome extensions.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://crxcavator.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `APPSTORE_ENTRY`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `LINKED_URL_INTERNAL`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`
- `PHYSICAL_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Module options

- `verify` — Verify identified hostnames resolve.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

CRXcavator automatically scans the entire Chrome Web Store every 3 hours and produces a quantified risk score for each Chrome Extension based on several factors.
