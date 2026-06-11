# NetworksDB

**Module ID:** `sfp_networksdb`

## Summary

Search NetworksDB.io API for IP address and domain information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://networksdb.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://networksdb.io/api/docs

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `NETBLOCK_MEMBER`
- `CO_HOSTED_SITE`
- `GEOINFO`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — NetworksDB API key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `delay` — Delay between requests, in seconds.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

Our database contains information about the public IPv4 and IPv6 addresses, networks and domains owned by companies and organisations across the world along with city-level IP geolocation data and autonomous system information.
