# Error String Extractor

**Module ID:** `sfp_errors`

## Summary

Identify common error messages in content like SQL errors, etc.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_errors
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_errors

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- **Produced:**
- `ERROR_MESSAGE`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Passive

## Test seeds

- `TARGET_WEB_CONTENT`: input=`Something went wrong: Internal Server Error` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify common error messages in content like SQL errors, etc.

**Module ID:** `sfp_errors`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT
**Produces:** ERROR_MESSAGE

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `Fatal error: undefined index in /var/www/html/index.php`
- Produced count: 0
