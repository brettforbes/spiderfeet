# Web Framework Identifier

**Module ID:** `sfp_webframework`

## Summary

Identify the usage of popular web frameworks like jQuery, YUI and others.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_webframework
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_webframework

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- **Produced:**
- `URL_WEB_FRAMEWORK`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Passive

## Test seeds

- `TARGET_WEB_CONTENT`: input=`<script src="/wp-includes/js/jquery.js"></script>` validation=smoke status=UNKNOWN; verdict=hit; produced=2

## Catalogue notes

Identify the usage of popular web frameworks like jQuery, YUI and others.

**Module ID:** `sfp_webframework`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT
**Produces:** URL_WEB_FRAMEWORK

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `<meta name="generator" content="WordPress 6.0" />`
- Produced count: 0
