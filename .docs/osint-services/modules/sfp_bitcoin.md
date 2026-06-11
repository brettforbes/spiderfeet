# Bitcoin Finder

**Module ID:** `sfp_bitcoin`

## Summary

Identify bitcoin addresses in scraped webpages.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_bitcoin
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_bitcoin

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- **Produced:**
- `BITCOIN_ADDRESS`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `TARGET_WEB_CONTENT`: input=`wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa on page` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify bitcoin addresses in scraped webpages.

**Module ID:** `sfp_bitcoin`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT
**Produces:** BITCOIN_ADDRESS

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa on page`
- Produced count: 1
