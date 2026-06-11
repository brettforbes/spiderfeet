# Onyphe

**Module ID:** `sfp_onyphe`

## Summary

Check Onyphe data (threat list, geo-location, pastries, vulnerabilities)  about a given IP.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.onyphe.io
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://www.onyphe.io/documentation/api

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `GEOINFO`
- `MALICIOUS_IPADDR`
- `LEAKSITE_CONTENT`
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`
- `VULNERABILITY_GENERAL`
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `PHYSICAL_COORDINATES`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Passive, Investigate

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `api_key` — Onyphe access token.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `max_page` — Maximum number of pages to iterate through. Onyphe has a maximum of 1000 pages (10,000 results). Only matters for paid plans
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `paid_plan` — Are you using paid plan? Paid plan has pagination enabled
- `verify` — Verify identified domains still resolve to the associated specified IP address.

## Catalogue notes

ONYPHE is a search engine for open-source and cyber threat intelligence data collected by crawling various sources available on the Internet or by listening to Internet background noise. They make this data available through API that we use. We check their data to see following information about the IP: geo-location, does it have some vulnerabilities, is it on some pastries (PasteBin) and is it on their threat list
