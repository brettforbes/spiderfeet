# Seon

**Module ID:** `sfp_seon`

## Summary

Queries seon.io to gather intelligence about IP Addresses, email addresses, and phone numbers

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://seon.io/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://docs.seon.io/api-reference

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `EMAILADDR`
- `PHONE_NUMBER`
- **Produced:**
- `GEOINFO`
- `MALICIOUS_IPADDR`
- `TCP_PORT_OPEN`
- `MALICIOUS_EMAILADDR`
- `EMAILADDR_DELIVERABLE`
- `EMAILADDR_UNDELIVERABLE`
- `SOCIAL_MEDIA`
- `HUMAN_NAME`
- `COMPANY_NAME`
- `EMAILADDR_COMPROMISED`
- `MALICIOUS_PHONE_NUMBER`
- `PROVIDER_TELCO`
- `PHONE_NUMBER_TYPE`
- `WEBSERVER_TECHNOLOGY`
- `RAW_RIR_DATA`
- `TOR_EXIT_NODE`
- `VPN_HOST`
- `PROXY_HOST`

## Flags and categories

- **Flags:** apikey
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — seon.io API Key
- `fraud_threshold` — Minimum fraud score for target to be marked as malicious (0-100)

## Catalogue notes

SEON Fraud Prevention tools help organisations reduce the costs and resources lost to fraud. Spot fake accounts, slash manual reviews and cut chargebacks now.
