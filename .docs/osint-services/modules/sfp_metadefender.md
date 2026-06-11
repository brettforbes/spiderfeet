# MetaDefender

**Module ID:** `sfp_metadefender`

## Summary

Search MetaDefender API for IP address and domain IP reputation.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://metadefender.opswat.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://onlinehelp.opswat.com/mdcloud/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `INTERNET_NAME`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_INTERNET_NAME`
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — MetaDefender API key.
- `delay` — Delay between requests, in seconds.

## Catalogue notes

File Analysis - Analyzing binaries with 30+ anti-malware engines.
Heuristic analysis to detect more unknown and targeted attacks.
Binary vulnerability data assessment, IP/Domain reputation, Threat Intelligence Feeds
