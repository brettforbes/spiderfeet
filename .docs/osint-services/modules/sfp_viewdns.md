# ViewDNS.info

**Module ID:** `sfp_viewdns`

## Summary

Identify co-hosted websites and perform reverse Whois lookups using ViewDNS.info.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://viewdns.info/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://viewdns.info/api/docs, https://viewdns.info/api/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `EMAILADDR`
- `IP_ADDRESS`
- `PROVIDER_DNS`
- **Produced:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `CO_HOSTED_SITE`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — ViewDNS.info API key.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

The ViewDNS.info API allows webmasters to integrate the tools provided by ViewDNS.info into their own sites in a simple and effective manner.
