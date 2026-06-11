# Hunter.io

**Module ID:** `sfp_hunter`

## Summary

Check for e-mail addresses and names on hunter.io.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://hunter.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://hunter.io/api

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Hunter.io API key.

## Catalogue notes

Hunter lets you find email addresses in seconds and connect with the people that matter for your business.
The Domain Search lists all the people working in a company with their name and email address found on the web. With 100+ million email addresses indexed, effective search filters and scoring, it's the most powerful email-finding tool ever created.
