# WiGLE

**Module ID:** `sfp_wigle`

## Summary

Query WiGLE to identify nearby WiFi access points.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://wigle.net/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://api.wigle.net/, https://api.wigle.net/swagger

## Routes

- **Route seed nugget:** `PHYSICAL_COORDINATES`
- **Consumed:**
- `PHYSICAL_COORDINATES`
- **Produced:**
- `WIFI_ACCESS_POINT`

## Flags and categories

- **Flags:** apikey
- **Categories:** Secondary Networks
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key_encoded` — Wigle.net base64-encoded API name/token pair.
- `days_limit` — Maximum age of data to be considered valid.
- `variance` — How tightly to bound queries against the latitude/longitude box extracted from idenified addresses. This value must be between 0.001 and 0.2.

## Catalogue notes

We consolidate location and information of wireless networks world-wide to a central database, and have user-friendly desktop and web applications that can map, query and update the database via the web.
