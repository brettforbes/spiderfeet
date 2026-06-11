# ipapi.co

**Module ID:** `sfp_ipapico`

## Summary

Queries ipapi.co to identify geolocation of IP Addresses using ipapi.co API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://ipapi.co/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ipapi.co/api/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `GEOINFO`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Catalogue notes

Powerful & Simple REST API for IP Address Geolocation.ipapi.co provides a REST API to find the location of an IP address.
