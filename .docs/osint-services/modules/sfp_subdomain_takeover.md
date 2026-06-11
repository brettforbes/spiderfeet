# Subdomain Takeover Checker

**Module ID:** `sfp_subdomain_takeover`

## Summary

Check if affiliated subdomains are vulnerable to takeover.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_subdomain_takeover
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_subdomain_takeover

## Routes

- **Route seed nugget:** `AFFILIATE_INTERNET_NAME`
- **Consumed:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`
- **Produced:**
- `AFFILIATE_INTERNET_NAME_HIJACKABLE`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Test seeds

- `AFFILIATE_INTERNET_NAME`: input=`affiliate.example.com` validation=smoke status=UNKNOWN; verdict=clean_miss; produced=0

## Catalogue notes

Check if affiliated subdomains are vulnerable to takeover.

**Module ID:** `sfp_subdomain_takeover`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** AFFILIATE_INTERNET_NAME, AFFILIATE_INTERNET_NAME_UNRESOLVED
**Produces:** AFFILIATE_INTERNET_NAME_HIJACKABLE

**Smoke battery:**
- Classification: `error_failed`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
