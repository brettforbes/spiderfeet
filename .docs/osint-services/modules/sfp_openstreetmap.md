# OpenStreetMap

**Module ID:** `sfp_openstreetmap`

## Summary

Retrieves latitude/longitude coordinates for physical addresses from OpenStreetMap API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://www.openstreetmap.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://wiki.openstreetmap.org/wiki/API, https://wiki.openstreetmap.org/wiki/API_v0.6

## Routes

- **Route seed nugget:** `PHYSICAL_ADDRESS`
- **Consumed:**
- `PHYSICAL_ADDRESS`
- **Produced:**
- `PHYSICAL_COORDINATES`

## Flags and categories

- **Flags:** —
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `PHYSICAL_ADDRESS`: input=`1600 Amphitheatre Parkway, Mountain View, CA 94043` validation=smoke status=FINISHED; verdict=hit; Pass 3 targeted probe; status=FINISHED

## Catalogue notes

OpenStreetMap powers map data on thousands of web sites, mobile apps, and hardware devices.
