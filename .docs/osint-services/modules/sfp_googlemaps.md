# Google Maps

**Module ID:** `sfp_googlemaps`

## Summary

Identifies potential physical addresses and latitude/longitude coordinates.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://cloud.google.com/maps-platform/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://developers.google.com/maps/documentation/?_ga=2.135220017.1220421370.1587340370-900596925.1587340370

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `PHYSICAL_ADDRESS`
- **Produced:**
- `PHYSICAL_ADDRESS`
- `PHYSICAL_COORDINATES`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Google Geocoding API Key.

## Catalogue notes

Explore where real-world insights and immersive location experiences can take your business.
Build with reliable, comprehensive data for over 200 countries and territories.
has been done here. If line breaks are needed for breaking up
Scale confidently, backed by our infrastructure.
