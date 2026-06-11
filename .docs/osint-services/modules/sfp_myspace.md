# MySpace

**Module ID:** `sfp_myspace`

## Summary

Gather username and location from MySpace.com profiles.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** https://myspace.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.programmableweb.com/api/myspace

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- `SOCIAL_MEDIA`
- **Produced:**
- `SOCIAL_MEDIA`
- `GEOINFO`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `EMAILADDR`: input=`noreply@spiderfoot.net` validation=blocked-upstream SPEC_GAP upstream: myspace.com search endpoint connection failures

## Catalogue notes

Myspace is a place where people come to connect, discover, and share.
Through an open design, compelling editorial features, and analytics-based recommendations, Myspace creates a creative community of people who connect around mutual affinity and inspiration for the purpose of shaping, sharing, and discovering what's next.
