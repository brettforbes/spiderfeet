# ReverseWhois

**Module ID:** `sfp_reversewhois`

## Summary

Reverse Whois lookups using reversewhois.io.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.reversewhois.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `DOMAIN_REGISTRAR`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

ReverseWhois is a free search engine to find domain names owned by an individual or company.
Search based on names or email addresses.
