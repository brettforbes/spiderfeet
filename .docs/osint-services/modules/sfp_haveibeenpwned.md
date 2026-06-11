# HaveIBeenPwned

**Module ID:** `sfp_haveibeenpwned`

## Summary

Check HaveIBeenPwned.com for hacked e-mail addresses identified in breaches.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://haveibeenpwned.com/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://haveibeenpwned.com/API/v3, https://haveibeenpwned.com/FAQs

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- `PHONE_NUMBER`
- **Produced:**
- `EMAILADDR_COMPROMISED`
- `PHONE_NUMBER_COMPROMISED`
- `LEAKSITE_CONTENT`
- `LEAKSITE_URL`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — HaveIBeenPwned.com API key.
