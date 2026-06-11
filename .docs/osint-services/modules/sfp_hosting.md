# Hosting Provider Identifier

**Module ID:** `sfp_hosting`

## Summary

Find out if any IP addresses identified fall within known 3rd party hosting ranges, e.g. Amazon, Azure, etc.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_hosting
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_hosting

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- **Produced:**
- `PROVIDER_HOSTING`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `IP_ADDRESS`: input=`3.8.0.0` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Find out if any IP addresses identified fall within known 3rd party hosting ranges, e.g. Amazon, Azure, etc.

**Module ID:** `sfp_hosting`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS
**Produces:** PROVIDER_HOSTING

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `Hosted on Amazon Web Services`
- Produced count: 0
