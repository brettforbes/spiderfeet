# GLEIF

**Module ID:** `sfp_gleif`

## Summary

Look up company information from Global Legal Entity Identifier Foundation (GLEIF).

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://search.gleif.org/
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** https://www.gleif.org/en/lei-data/gleif-api, https://api.gleif.org/docs

## Routes

- **Route seed nugget:** `COMPANY_NAME`
- **Consumed:**
- `COMPANY_NAME`
- `LEI`
- **Produced:**
- `COMPANY_NAME`
- `LEI`
- `PHYSICAL_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Passive, Footprint, Investigate

## Test seeds

- `COMPANY_NAME`: input=`Google LLC` validation=smoke status=FINISHED; verdict=hit; Pass 3 targeted probe; status=FINISHED

## Catalogue notes

The Global Legal Entity Identifier Foundation (GLEIF) Global LEI Index contains historical and current LEI records including related reference data in one authoritative, central repository.
