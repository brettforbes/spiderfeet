# Social Links

**Module ID:** `sfp_sociallinks`

## Summary

Queries SocialLinks.io to gather intelligence from social media platforms and dark web.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://sociallinks.io/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://docs.osint.rest/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `USERNAME`
- `EMAILADDR`
- `PHONE_NUMBER`
- **Produced:**
- `GEOINFO`
- `SOCIAL_MEDIA`
- `HUMAN_NAME`
- `JOB_TITLE`
- `COMPANY_NAME`
- `PHONE_NUMBER`
- `ACCOUNT_EXTERNAL_OWNED`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Social Links API Key

## Catalogue notes

Social Links provides instruments for OSINT methods that are used by the world's leading investigation and law enforcement agencies
