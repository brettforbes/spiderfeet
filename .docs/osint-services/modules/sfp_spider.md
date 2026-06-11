# Web Spider

**Module ID:** `sfp_spider`

## Summary

Spidering of web-pages to extract content for searching.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_spider
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_spider

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- `INTERNET_NAME`
- **Produced:**
- `WEBSERVER_HTTPHEADERS`
- `HTTP_CODE`
- `LINKED_URL_INTERNAL`
- `LINKED_URL_EXTERNAL`
- `TARGET_WEB_CONTENT`
- `TARGET_WEB_CONTENT_TYPE`

## Flags and categories

- **Flags:** slow
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `filterfiles` — File extensions to ignore (don't fetch them.)
- `filtermime` — MIME types to ignore.
- `filterusers` — Skip spidering of /~user directories?
- `maxlevels` — Maximum levels to traverse per starting point (e.g. hostname or link identified by another module) identified.
- `maxpages` — Maximum number of pages to fetch per starting point identified.
- `nosubs` — Skip spidering of subdomains of the target?
- `pausesec` — Number of seconds to pause between page fetches.
- `reportduplicates` — Report links every time one is found, even if found before?
- `robotsonly` — Only follow links specified by robots.txt?
- `start` — Prepend targets with these until you get a hit, to start spidering.
- `usecookies` — Accept and use cookies?

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=7

## Catalogue notes

Spidering of web-pages to extract content for searching.

**Module ID:** `sfp_spider`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL, INTERNET_NAME
**Produces:** WEBSERVER_HTTPHEADERS, HTTP_CODE, LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL, TARGET_WEB_CONTENT, TARGET_WEB_CONTENT_TYPE
**Flags:** slow

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 7
