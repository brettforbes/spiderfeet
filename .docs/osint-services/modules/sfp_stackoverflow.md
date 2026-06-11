# StackOverflow

**Module ID:** `sfp_stackoverflow`

## Summary

Search StackOverflow for any mentions of a target domain. Returns potentially related information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.stackexchange.com
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** https://api.stackexchange.com/docs

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `EMAILADDR`
- `AFFILIATE_EMAILADDR`
- `USERNAME`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `HUMAN_NAME`

## Flags and categories

- **Flags:** errorprone, apikey
- **Categories:** Content Analysis
- **Use cases:** Passive

## Module options

- `api_key` — StackApps has an optional API key. Using an API key will increase the amount of requests allowed.

## Catalogue notes

StackOverflow is a knowledge sharing public platform for IT professionalsand students where users can post questions and get answers from other users.
