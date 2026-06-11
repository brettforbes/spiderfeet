# Ethereum Address Extractor

**Module ID:** `sfp_ethereum`

## Summary

Identify ethereum addresses in scraped webpages.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_ethereum
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_ethereum

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- **Produced:**
- `ETHEREUM_ADDRESS`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `TARGET_WEB_CONTENT`: input=`send to 0x0000000000000000000000000000000000000000` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify ethereum addresses in scraped webpages.

**Module ID:** `sfp_ethereum`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT
**Produces:** ETHEREUM_ADDRESS

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `send to 0x0000000000000000000000000000000000000000`
- Produced count: 1
