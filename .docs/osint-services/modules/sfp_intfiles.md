# Interesting File Finder

**Module ID:** `sfp_intfiles`

## Summary

Identifies potential files of interest, e.g. office documents, zip files.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_intfiles
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_intfiles

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- **Produced:**
- `INTERESTING_FILE`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Passive

## Module options

- `fileexts` — File extensions of files you consider interesting.

## Test seeds

- `LINKED_URL_INTERNAL`: input=`https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identifies potential files of interest, e.g. office documents, zip files.

**Module ID:** `sfp_intfiles`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL
**Produces:** INTERESTING_FILE

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `LINKED_URL_INTERNAL`
- Input: `https://example.com/robots.txt`
- Produced count: 0
