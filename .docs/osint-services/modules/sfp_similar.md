# Similar Domain Finder

**Module ID:** `sfp_similar`

## Summary

Search various sources to identify similar looking domain names, for instance squatted domains.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_similar
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_similar

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `SIMILARDOMAIN`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Module options

- `skipwildcards` — Skip TLDs and sub-TLDs that have wildcard DNS.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=61

## Catalogue notes

Search various sources to identify similar looking domain names, for instance squatted domains.

**Module ID:** `sfp_similar`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** DOMAIN_NAME
**Produces:** SIMILARDOMAIN

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 61
