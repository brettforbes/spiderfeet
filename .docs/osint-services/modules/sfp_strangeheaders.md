# Strange Header Identifier

**Module ID:** `sfp_strangeheaders`

## Summary

Obtain non-standard HTTP headers returned by web servers.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_strangeheaders
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_strangeheaders

## Routes

- **Route seed nugget:** `WEBSERVER_HTTPHEADERS`
- **Consumed:**
- `WEBSERVER_HTTPHEADERS`
- **Produced:**
- `WEBSERVER_STRANGEHEADER`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Passive

## Test seeds

- `WEBSERVER_HTTPHEADERS`: input=`{"x-powered-by": "PHP/7.4", "x-obscure-header": "test"}` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Obtain non-standard HTTP headers returned by web servers.

**Module ID:** `sfp_strangeheaders`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** WEBSERVER_HTTPHEADERS
**Produces:** WEBSERVER_STRANGEHEADER

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `WEBSERVER_HTTPHEADERS`
- Input: `X-Powered-By: PHP/7.4
X-Obscure-Header: test`
- Produced count: 0
