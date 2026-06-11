# SpyOnWeb

**Module ID:** `sfp_spyonweb`

## Summary

Search SpyOnWeb for hosts sharing the same IP address, Google Analytics code, or Google Adsense code.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** http://spyonweb.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://api.spyonweb.com/v1/docs, https://api.spyonweb.com/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `WEB_ANALYTICS_ID`
- **Produced:**
- `CO_HOSTED_SITE`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `WEB_ANALYTICS_ID`
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — SpyOnWeb API key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `limit` — Maximum number of results to fetch.
- `maxage` — The maximum age of the data returned, in days, in order to be considered valid.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `timeout` — Query timeout, in seconds.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

We take the information from public sources, then structure it for your quick and convenient search for the websites that probably belong to the same owner.
