# RiskIQ

**Module ID:** `sfp_riskiq`

## Summary

Obtain information from RiskIQ's (formerly PassiveTotal) Passive DNS and Passive SSL databases.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://community.riskiq.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://info.riskiq.net/help, https://www.riskiq.com/resources/?type=training_videos, https://api.riskiq.net/api/concepts.html

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `DOMAIN_NAME`
- `EMAILADDR`
- **Produced:**
- `IP_ADDRESS`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `CO_HOSTED_SITE`
- `NETBLOCK_OWNER`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `api_key_login` — RiskIQ login.
- `api_key_password` — RiskIQ API Key.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

RiskIQ Community brings petabytes of internet intelligence directly to your fingertips. Investigate threats by pivoting through attacker infrastructure data. Understand your digital assets that are internet-exposed, and map and monitor your external attack surface.
