# Credit Card Number Extractor

**Module ID:** `sfp_creditcard`

## Summary

Identify Credit Card Numbers in any data

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_creditcard
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_creditcard

## Routes

- **Route seed nugget:** `DARKNET_MENTION_CONTENT`
- **Consumed:**
- `DARKNET_MENTION_CONTENT`
- `LEAKSITE_CONTENT`
- **Produced:**
- `CREDIT_CARD_NUMBER`

## Flags and categories

- **Flags:** errorprone
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DARKNET_MENTION_CONTENT`: input=`card 4111111111111111 expires 12/30` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify Credit Card Numbers in any data

**Module ID:** `sfp_creditcard`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** DARKNET_MENTION_CONTENT, LEAKSITE_CONTENT
**Produces:** CREDIT_CARD_NUMBER
**Flags:** errorprone

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `DARKNET_MENTION_CONTENT`
- Input: `card 4111111111111111 expires 12/30`
- Produced count: 1
