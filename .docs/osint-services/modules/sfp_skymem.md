# Skymem

**Module ID:** `sfp_skymem`

## Summary

Look up e-mail addresses on Skymem.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://www.skymem.info/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** http://www.skymem.info/faq

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)
