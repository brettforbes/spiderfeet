# FullContact

**Module ID:** `sfp_fullcontact`

## Summary

Gather domain and e-mail information from FullContact.com API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.fullcontact.com
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://dashboard.fullcontact.com/api-ref, https://www.fullcontact.com/developer-portal/, https://www.fullcontact.com/insights-bundles/, https://dashboard.fullcontact.com/docs, https://www.fullcontact.com/faq/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `EMAILADDR`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `RAW_RIR_DATA`
- `PHONE_NUMBER`
- `GEOINFO`
- `PHYSICAL_ADDRESS`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — FullContact.com API key.
- `max_age_days` — Maximum number of age in days for a record before it's considered invalid and not reported.

## Catalogue notes

Connecting data. Consolidating identities. Applying insights. Amplifying media reach. We provide person-centered identity resolution to improve your customer interactions with a simple, real-time API integration.
FullContact is a privacy-safe Identity Resolution company building trust between people and brands. We deliver the capabilities needed to create tailored customer experiences by unifying data and applying insights in the moments that matter.
