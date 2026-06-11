# ipapi.com

**Module ID:** `sfp_ipapicom`

## Summary

Queries ipapi.com to identify geolocation of IP Addresses using ipapi.com API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://ipapi.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ipapi.com/documentation

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `GEOINFO`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — ipapi.com API Key.

## Catalogue notes

ipapi provides an easy-to-use API interface allowing customers to look various pieces of information IPv4 and IPv6 addresses are associated with. For each IP address processed, the API returns more than 45 unique data points, such as location data, connection data, ISP information, time zone, currency and security assessment data.
