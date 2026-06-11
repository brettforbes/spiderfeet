# FullHunt

**Module ID:** `sfp_fullhunt`

## Summary

Identify domain attack surface using FullHunt API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://fullhunt.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://api-docs.fullhunt.io/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`
- `TCP_PORT_OPEN`
- `PROVIDER_DNS`
- `PROVIDER_MAIL`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `api_key` — FullHunt API key.

## Catalogue notes

Discover, monitor, and secure your attack surface. FullHunt delivers the best platform in the market for attack surface security.
