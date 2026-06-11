# Focsec

**Module ID:** `sfp_focsec`

## Summary

Look up IP address information from Focsec.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://focsec.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.focsec.com/#ip

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`
- `MALICIOUS_IPADDR`
- `PROXY_HOST`
- `VPN_HOST`
- `TOR_EXIT_NODE`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `api_key` — Focsec API Key.

## Catalogue notes

Our API lets you know if a user's IP address is associated with a VPN, Proxy, TOR or malicious bots.Take your applications security to the next level by detecting suspicious activity early on.
