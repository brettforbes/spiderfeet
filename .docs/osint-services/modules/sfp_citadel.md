# Leak-Lookup

**Module ID:** `sfp_citadel`

## Summary

Searches Leak-Lookup.com's database of breaches.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://leak-lookup.com/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://leak-lookup.com/api, https://leak-lookup.com/databases

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `EMAILADDR_COMPROMISED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Leak-Lookup API key. Without this you're limited to the public API.
- `timeout` — Custom timeout due to heavy traffic at times.

## Catalogue notes

Leak-Lookup allows you to search across thousands of data breaches to stay on top of credentials that may have been compromised in the wild.
The creators came together when they realized they had a vast trove of data that could be of great value to pen-testers seeking weaknesses in client passwords and those concerned about which of their credentials have been leaked into the wild.
Always looking forward, Leak-Lookup invests all of its profits back into securing the latest data breaches and leaks / dumps as they become available, ensuring that as well as historical data, Leak-Lookup becomes a field leader in credential monitoring.
