# ZoneFile.io

**Module ID:** `sfp_zonefiles`

## Summary

Search ZoneFiles.io Domain query API for domain information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://zonefiles.io
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://zonefiles.io/query-api/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `IP_ADDRESS`
- `PHONE_NUMBER`
- `EMAILADDR`
- `PROVIDER_DNS`
- `SOFTWARE_USED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — ZoneFiles.io API key.
- `delay` — Delay between requests, in seconds.
- `verify` — Verify specified domains still resolve to the identified IP address.
