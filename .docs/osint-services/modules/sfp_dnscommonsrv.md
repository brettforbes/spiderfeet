# DNS Common SRV

**Module ID:** `sfp_dnscommonsrv`

## Summary

Attempts to identify hostnames through brute-forcing common DNS SRV records.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_dnscommonsrv
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnscommonsrv

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`

## Flags and categories

- **Flags:** slow
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Test seeds

- `DOMAIN_NAME`: input=`microsoft.com` validation=smoke status=UNKNOWN; verdict=hit; produced=4

## Catalogue notes

Attempts to identify hostnames through brute-forcing common DNS SRV records.

**Module ID:** `sfp_dnscommonsrv`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, DOMAIN_NAME
**Produces:** INTERNET_NAME, AFFILIATE_INTERNET_NAME
**Flags:** slow

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 0
