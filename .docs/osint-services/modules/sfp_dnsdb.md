# DNSDB

**Module ID:** `sfp_dnsdb`

## Summary

Query FarSight's DNSDB for historical and passive DNS data.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.farsightsecurity.com
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.dnsdb.info/dnsdb-apiv2/, https://www.farsightsecurity.com/get-started/https://www.farsightsecurity.com/solutions/dnsdb/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `PROVIDER_DNS`
- `DNS_TEXT`
- `PROVIDER_MAIL`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `CO_HOSTED_SITE`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `age_limit_days` — Ignore any DNSDB records older than this many days. 0 = unlimited.
- `api_key` — DNSDB API Key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

Farsight Security’s DNSDB is the world’s largest database of DNS resolution and change data. Started in 2010 and updated in real-time, DNSDB provides the most comprehensive history of domains and IP addresses worldwide.
