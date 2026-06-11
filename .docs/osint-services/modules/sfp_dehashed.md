# Dehashed

**Module ID:** `sfp_dehashed`

## Summary

Gather breach data from Dehashed API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.dehashed.com/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://www.dehashed.com/docs

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `EMAILADDR`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_COMPROMISED`
- `PASSWORD_COMPROMISED`
- `HASH_COMPROMISED`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Dehashed API key.
- `api_key_username` — Dehashed username.
- `max_pages` — Maximum number of pages to fetch(Max: 10 pages)
- `pause` — Number of seconds to wait between each API call.
- `per_page` — Maximum number of results per page.(Max: 10000)

## Catalogue notes

Have you been compromised? DeHashed provides free deep-web scans and protection against credential leaks. A modern personal asset search engine created for security analysts, journalists, security companies, and everyday people to help secure accounts and provide insight on compromised assets. Free breach alerts & breach notifications.
