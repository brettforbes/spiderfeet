# EmailCrawlr

**Module ID:** `sfp_emailcrawlr`

## Summary

Search EmailCrawlr for email addresses and phone numbers associated with a domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://emailcrawlr.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://emailcrawlr.com/docs

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `PHONE_NUMBER`
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — EmailCrawlr API key.
- `delay` — Delay between requests, in seconds.

## Catalogue notes

By using the EmailCrawlr JSON API you can: Get key information about company websites.
Find all email addresses associated with a domain.
Get social accounts associated with an email.
Verify email address deliverability.
