# C99

**Module ID:** `sfp_c99`

## Summary

Queries the C99 API which offers various data (geo location, proxy detection, phone lookup, etc).

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://api.c99.nl/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://api.c99.nl/api_overview, https://api.c99.nl/faq

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `PHONE_NUMBER`
- `IP_ADDRESS`
- `USERNAME`
- `EMAILADDR`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `PROVIDER_TELCO`
- `PHYSICAL_ADDRESS`
- `PHYSICAL_COORDINATES`
- `PROVIDER_DNS`
- `IP_ADDRESS`
- `USERNAME`
- `ACCOUNT_EXTERNAL_OWNED`
- `WEBSERVER_TECHNOLOGY`
- `PROVIDER_HOSTING`
- `CO_HOSTED_SITE`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Passive, Investigate

## Module options

- `api_key` — C99 API Key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify identified domains still resolve to the associated specified IP address.

## Catalogue notes

C99 API service is versatile source of information. They offer over 57 different APIs of which 10 are integrated in this module. APIs that are integrated are subdomain finder, phone lookup, Skype resolver, IP to Skype, firewall technology WAF detector, domain history, IP to domains, IP geo location, proxy detector.
