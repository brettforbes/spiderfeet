# IPInfo.io

**Module ID:** `sfp_ipinfo`

## Summary

Identifies the physical location of IP addresses identified using ipinfo.io.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://ipinfo.io
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ipinfo.io/developers

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Ipinfo.io access token.

## Catalogue notes

The Trusted Source for IP Address Data.
With IPinfo, you can pinpoint your users’ locations, customize their experiences, prevent fraud, ensure compliance, and so much more.
