# Debounce

**Module ID:** `sfp_debounce`

## Summary

Check whether an email is disposable

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://debounce.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://debounce.io/free-disposable-check-api/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `EMAILADDR_DISPOSABLE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `EMAILADDR`: input=`noreply@spiderfoot.net` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

DeBounce provides a free & powerful API endpoint for checking a domain or email address against a realtime up-to-date list of disposable domains.CORS is enabled for all originating domains, so you can call the API directly from your client-side code.
