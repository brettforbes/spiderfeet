# IBAN Number Extractor

**Module ID:** `sfp_iban`

## Summary

Identify International Bank Account Numbers (IBANs) in any data.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_iban
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_iban

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `DARKNET_MENTION_CONTENT`
- `LEAKSITE_CONTENT`
- **Produced:**
- `IBAN_NUMBER`

## Flags and categories

- **Flags:** errorprone
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DARKNET_MENTION_CONTENT`: input=`IBAN GB82WEST12345698765432` validation=smoke smoke
- `TARGET_WEB_CONTENT`: input=`DE89370400440532013000` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify International Bank Account Numbers (IBANs) in any data.

**Module ID:** `sfp_iban`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, DARKNET_MENTION_CONTENT, LEAKSITE_CONTENT
**Produces:** IBAN_NUMBER
**Flags:** errorprone

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `DARKNET_MENTION_CONTENT`
- Input: `IBAN GB82WEST12345698765432`
- Produced count: 0
