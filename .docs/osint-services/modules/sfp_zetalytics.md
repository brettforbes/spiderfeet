# Zetalytics

**Module ID:** `sfp_zetalytics`

## Summary

Query the Zetalytics database for hosts on your target domain(s).

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://zetalytics.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://zonecruncher.com/api-v1-docs/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `EMAILADDR`
- **Produced:**
- `INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Passive

## Module options

- `api_key` — Zetalytics API Key.
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Catalogue notes

Zetalytics database provides several useful endpoints to perform passive DNS analysis
