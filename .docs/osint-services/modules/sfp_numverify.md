# numverify

**Module ID:** `sfp_numverify`

## Summary

Lookup phone number location and carrier information from numverify.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** http://numverify.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://numverify.com/documentation, https://numverify.com/faq

## Routes

- **Route seed nugget:** `PHONE_NUMBER`
- **Consumed:**
- `PHONE_NUMBER`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`
- `PROVIDER_TELCO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — numverify API key.

## Catalogue notes

Global Phone Number Validation & Lookup JSON API.
NumVerify offers a full-featured yet simple RESTful JSON API for national and international phone number validation and information lookup for a total of 232 countries around the world.
Requested numbers are processed in real-time, cross-checked with the latest international numbering plan databases and returned in handy JSON format enriched with useful carrier, geographical location and line type data.
