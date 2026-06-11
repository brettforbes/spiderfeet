# SecurityTrails

**Module ID:** `sfp_securitytrails`

## Summary

Obtain Passive DNS and other information from SecurityTrails

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://securitytrails.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.securitytrails.com/docs, https://docs.securitytrails.com/reference#general

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `DOMAIN_NAME`
- `EMAILADDR`
- `NETBLOCK_OWNER`
- **Produced:**
- `CO_HOSTED_SITE`
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `PROVIDER_HOSTING`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — SecurityTrails API key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

Data for Security companies, researchers and teams. Fast, always up API that allows you to access current and historical data. The API is paid via a simple pricing structure that allows you to embed our data into your applications.
Search nearly 3 billion historical and current WHOIS data and WHOIS changes.
