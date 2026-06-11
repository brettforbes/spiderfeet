# Junk File Finder

**Module ID:** `sfp_junkfiles`

## Summary

Looks for old/temporary and other similar files.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_junkfiles
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_junkfiles

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- **Produced:**
- `JUNK_FILE`

## Flags and categories

- **Flags:** slow, errorprone, invasive
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint

## Module options

- `dirs` — Try to fetch the containing folder with these extensions.
- `fileexts` — File extensions to try.
- `files` — Try to fetch each of these files from the directory of the URL.
- `urlextstry` — Try those extensions against URLs with these extensions.

## Test seeds

- `LINKED_URL_INTERNAL`: input=`https://example.com/` validation=smoke status=UNKNOWN; verdict=clean_miss; produced=0

## Catalogue notes

Looks for old/temporary and other similar files.

**Module ID:** `sfp_junkfiles`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL
**Produces:** JUNK_FILE
**Flags:** slow, errorprone, invasive

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
