# EmailFormat

**Module ID:** `sfp_emailformat`

## Summary

Look up e-mail addresses on email-format.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.email-format.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.email-format.com/i/api_access/, https://www.email-format.com/i/api_v2/, https://www.email-format.com/i/api_v1/

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

## Catalogue notes

Save time and energy - find the email address formats in use at thousands of companies.
