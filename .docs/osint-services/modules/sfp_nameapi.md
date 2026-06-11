# NameAPI

**Module ID:** `sfp_nameapi`

## Summary

Check whether an email is disposable

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.nameapi.org/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://www.nameapi.org/en/developer/manuals/rest-web-services/53/web-services/disposable-email-address-detector/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `EMAILADDR_DISPOSABLE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — API Key for NameAPI

## Catalogue notes

The NameAPI DEA-Detector checks email addresses against a list of known trash domains such as mailinator.com.
It classifies those as disposable which operate as a time-limited, web based way of receiving emails, for example, sign up confirmations.
