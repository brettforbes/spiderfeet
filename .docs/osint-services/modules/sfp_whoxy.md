# Whoxy

**Module ID:** `sfp_whoxy`

## Summary

Reverse Whois lookups using Whoxy.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.whoxy.com/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://www.whoxy.com/#api, https://www.whoxy.com/whois-history/, https://www.whoxy.com/free-whois-api/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — Whoxy.com API key.

## Catalogue notes

Whois API is a hosted web service that returns well-parsed WHOIS fields to your application in popular XML & JSON formats per HTTP request. Leave all the hard work to us, as you need not worry about the query limit and restrictions imposed by various domain registrars.
