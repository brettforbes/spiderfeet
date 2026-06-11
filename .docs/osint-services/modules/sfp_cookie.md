# Cookie Extractor

**Module ID:** `sfp_cookie`

## Summary

Extract Cookies from HTTP headers.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_cookie
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_cookie

## Routes

- **Route seed nugget:** `WEBSERVER_HTTPHEADERS`
- **Consumed:**
- `WEBSERVER_HTTPHEADERS`
- **Produced:**
- `TARGET_WEB_COOKIE`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `WEBSERVER_HTTPHEADERS`: input=`{"cookie": "sessionid=abc123; Path=/; HttpOnly"}` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Extract Cookies from HTTP headers.

**Module ID:** `sfp_cookie`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** WEBSERVER_HTTPHEADERS
**Produces:** TARGET_WEB_COOKIE

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `WEBSERVER_HTTPHEADERS`
- Input: `Set-Cookie: sessionid=abc123; Path=/; HttpOnly`
- Produced count: 0
