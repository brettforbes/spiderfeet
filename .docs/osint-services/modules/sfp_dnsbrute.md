# DNS Brute-forcer

**Module ID:** `sfp_dnsbrute`

## Summary

Attempts to identify hostnames through brute-forcing common names and iterations.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_dnsbrute
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnsbrute

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `INTERNET_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Module options

- `_maxthreads` — Maximum threads
- `commons` — Try a list of about 750 common hostnames/sub-domains.
- `domainonly` — Only attempt to brute-force names on domain names, not hostnames (some hostnames are also sub-domains).
- `numbersuffix` — For any host found, try appending 1, 01, 001, -1, -01, -001, 2, 02, etc. (up to 10)
- `numbersuffixlimit` — Limit using the number suffixes for hosts that have already been resolved? If disabled this will significantly extend the duration of scans.
- `skipcommonwildcard` — If wildcard DNS is detected, don't bother brute-forcing.
- `top10000` — Try a further 10,000 common hostnames/sub-domains. Will make the scan much slower.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Attempts to identify hostnames through brute-forcing common names and iterations.

**Module ID:** `sfp_dnsbrute`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** DOMAIN_NAME, INTERNET_NAME
**Produces:** INTERNET_NAME

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 1
