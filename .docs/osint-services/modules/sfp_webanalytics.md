# Web Analytics Extractor

**Module ID:** `sfp_webanalytics`

## Summary

Identify web analytics IDs in scraped webpages and DNS TXT records.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_webanalytics
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_webanalytics

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `DNS_TEXT`
- **Produced:**
- `WEB_ANALYTICS_ID`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DNS_TEXT`: input=`google-site-verification=abc123` validation=smoke smoke
- `TARGET_WEB_CONTENT`: input=`<script>ga("create", "UA-40102974-1", "auto");</script>` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify web analytics IDs in scraped webpages and DNS TXT records.

**Module ID:** `sfp_webanalytics`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, DNS_TEXT
**Produces:** WEB_ANALYTICS_ID

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `DNS_TEXT`
- Input: `google-site-verification=abc123`
- Produced count: 0
