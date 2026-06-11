# Page Information

**Module ID:** `sfp_pageinfo`

## Summary

Obtain information about web pages (do they take passwords, do they contain forms, etc.)

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_pageinfo
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_pageinfo

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- **Produced:**
- `URL_STATIC`
- `URL_JAVASCRIPT`
- `URL_FORM`
- `URL_PASSWORD`
- `URL_UPLOAD`
- `URL_JAVA_APPLET`
- `URL_FLASH`
- `PROVIDER_JAVASCRIPT`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `TARGET_WEB_CONTENT`: input=`<title>Example Domain</title>` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Obtain information about web pages (do they take passwords, do they contain forms, etc.)

**Module ID:** `sfp_pageinfo`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT
**Produces:** URL_STATIC, URL_JAVASCRIPT, URL_FORM, URL_PASSWORD, URL_UPLOAD, URL_JAVA_APPLET, URL_FLASH, PROVIDER_JAVASCRIPT

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `<title>Example Domain</title>`
- Produced count: 0
