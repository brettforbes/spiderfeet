# BuiltWith

**Module ID:** `sfp_builtwith`

## Summary

Query BuiltWith.com's Domain API for information about your target's web technology stack, e-mail addresses and more.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://builtwith.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://api.builtwith.com/, https://kb.builtwith.com/, https://builtwith.com/screencast, https://builtwith.com/faq

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `RAW_RIR_DATA`
- `WEBSERVER_TECHNOLOGY`
- `PHONE_NUMBER`
- `DOMAIN_NAME`
- `CO_HOSTED_SITE`
- `IP_ADDRESS`
- `WEB_ANALYTICS_ID`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Builtwith.com Domain API key.
- `maxage` — The maximum age of the data returned, in days, in order to be considered valid.

## Catalogue notes

Build lists of websites from our database of 38,701+ web technologies and over a quarter of a billion websites showing which sites use shopping carts, analytics, hosting and many more. Filter by location, traffic, vertical and more.
Know your prospects platform before you talk to them. Improve your conversions with validated market adoption.
Get advanced technology market share information and country based analytics for all web technologies.
