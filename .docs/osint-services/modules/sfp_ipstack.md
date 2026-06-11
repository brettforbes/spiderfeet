# ipstack

**Module ID:** `sfp_ipstack`

## Summary

Identifies the physical location of IP addresses identified using ipstack.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://ipstack.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ipstack.com/documentation, https://ipstack.com/faq

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- **Produced:**
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Ipstack.com API key.

## Catalogue notes

Locate and identify website visitors by IP address.
ipstack offers one of the leading IP to geolocation APIS and global IP database services worldwide.
