# Iknowwhatyoudownload.com

**Module ID:** `sfp_iknowwhatyoudownload`

## Summary

Check iknowwhatyoudownload.com for IP addresses that have been using torrents.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://iknowwhatyoudownload.com/en/peer/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://iknowwhatyoudownload.com/en/api/, https://iknowwhatyoudownload.com/en/link/, https://iknowwhatyoudownload.com/en/peer/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `MALICIOUS_IPADDR`

## Flags and categories

- **Flags:** apikey
- **Categories:** Secondary Networks
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Iknowwhatyoudownload.com API key.
- `daysback` — How far back (in days) to look for activity.

## Catalogue notes

Our system collects torrent files in two ways: parsing torrent sites, and listening DHT network. The system contains more than 7 million torrents (as of Oct 2021) which were classified and which are using now for collecting peer sharing facts (up to 200.000.000 daily).
