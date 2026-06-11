# OpenCorporates

**Module ID:** `sfp_opencorporates`

## Summary

Look up company information from OpenCorporates.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://opencorporates.com
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** https://api.opencorporates.com/documentation/API-Reference

## Routes

- **Route seed nugget:** `COMPANY_NAME`
- **Consumed:**
- `COMPANY_NAME`
- **Produced:**
- `COMPANY_NAME`
- `PHYSICAL_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `api_key` — OpenCorporates.com API key. Without this you will be limited to 50 look-ups per day.
- `confidence` — Confidence that the search result objects are correct (numeric value between 0 and 100).

## Catalogue notes

The largest open database of companies in the world.
As the largest, open database of companies in the world, our business is making high-quality, official company data openly available. Data that can be trusted, accessed, analysed and interrogated when and how it’s needed.
