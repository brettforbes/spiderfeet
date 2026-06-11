# LeakIX

**Module ID:** `sfp_leakix`

## Summary

Search LeakIX for host data leaks, open ports, software and geoip.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://leakix.net/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://leakix.net/api-documentation

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`
- `TCP_PORT_OPEN`
- `OPERATING_SYSTEM`
- `SOFTWARE_USED`
- `WEBSERVER_BANNER`
- `LEAKSITE_CONTENT`
- `INTERNET_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — LeakIX API key
- `delay` — Delay between requests, in seconds.
- `verify` — Verify discovered hostnames are valid by checking if they still resolve.

## Catalogue notes

LeakIX provides insights into devices and servers that are compromised and compromised database schemas online.
In this scope we inspect found services for weak credentials.
