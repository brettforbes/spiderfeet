# Github

**Module ID:** `sfp_github`

## Summary

Identify associated public code repositories on Github.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://github.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://developer.github.com/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `USERNAME`
- `SOCIAL_MEDIA`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`
- `PUBLIC_CODE_REPO`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Passive

## Module options

- `namesonly` — Match repositories by name only, not by their descriptions. Helps reduce false positives.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

GitHub brings together the world's largest community of developers to discover, share, and build better software.
