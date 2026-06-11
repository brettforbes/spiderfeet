# AbstractAPI

**Module ID:** `sfp_abstractapi`

## Summary

Look up domain, phone, IP, and email reputation information from AbstractAPI.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://app.abstractapi.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://app.abstractapi.com/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `PHONE_NUMBER`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `EMAILADDR`
- **Produced:**
- `COMPANY_NAME`
- `SOCIAL_MEDIA`
- `GEOINFO`
- `PHYSICAL_COORDINATES`
- `PROVIDER_TELCO`
- `RAW_RIR_DATA`
- `EMAILADDR_DELIVERABLE`
- `EMAILADDR_UNDELIVERABLE`
- `EMAILADDR_DISPOSABLE`
- `EMAILADDR_COMPROMISED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `companyenrichment_api_key` — AbstractAPI Company Enrichment API key.
- `ipgeolocation_api_key` — AbstractAPI IP Geolocation API key.
- `phonevalidation_api_key` — AbstractAPI Phone Validation API key.
- `emailreputation_api_key` — AbstractAPI Email Reputation API key.

## Catalogue notes

Abstract provides powerful APIs to help you enrich any user experience or automate any workflow.
