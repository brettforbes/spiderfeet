# Web Server Identifier

**Module ID:** `sfp_webserver`

## Summary

Obtain web server banners to identify versions of web servers being used.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_webserver
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_webserver

## Routes

- **Route seed nugget:** `WEBSERVER_HTTPHEADERS`
- **Consumed:**
- `WEBSERVER_HTTPHEADERS`
- **Produced:**
- `WEBSERVER_BANNER`
- `WEBSERVER_TECHNOLOGY`
- `LINKED_URL_INTERNAL`
- `LINKED_URL_EXTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `WEBSERVER_HTTPHEADERS`: input=`{"server": "Apache/2.4.57"}` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Obtain web server banners to identify versions of web servers being used.

**Module ID:** `sfp_webserver`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** WEBSERVER_HTTPHEADERS
**Produces:** WEBSERVER_BANNER, WEBSERVER_TECHNOLOGY, LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `WEBSERVER_HTTPHEADERS`
- Input: `Server: Apache/2.4.57 (Ubuntu)`
- Produced count: 0
