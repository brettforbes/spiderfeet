# IPQualityScore

**Module ID:** `sfp_ipqualityscore`

## Summary

Determine if target is malicious using IPQualityScore API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.ipqualityscore.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://www.ipqualityscore.com/documentation/overview

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `EMAILADDR`
- `IP_ADDRESS`
- `PHONE_NUMBER`
- **Produced:**
- `EMAILADDR_DISPOSABLE`
- `EMAILADDR_COMPROMISED`
- `GEOINFO`
- `MALICIOUS_PHONE_NUMBER`
- `MALICIOUS_EMAILADDR`
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `PHONE_NUMBER_TYPE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `abuse_score_threshold` — Minimum abuse score for target to be considered malicious (0 - 100)
- `api_key` — IPQualityScore API Key
- `strictness` — Depth of the reputation checks to be performed on the target (0 - 2)

## Catalogue notes

IPQualityScore's suite of fraud prevention tools automate quality control to prevent bots, fake accounts, fraudsters, suspicious transactions, & malicious users without interrupting the user experience.
