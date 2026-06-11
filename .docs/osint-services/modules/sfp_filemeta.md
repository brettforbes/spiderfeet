# File Metadata Extractor

**Module ID:** `sfp_filemeta`

## Summary

Extracts meta data from documents and images.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_filemeta
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_filemeta

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- `INTERESTING_FILE`
- **Produced:**
- `RAW_FILE_META_DATA`
- `SOFTWARE_USED`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint

## Module options

- `fileexts` — File extensions of files you want to analyze the meta data of (only PDF, DOCX, XLSX and PPTX are supported.)
- `timeout` — Download timeout for files, in seconds.

## Test seeds

- `LINKED_URL_INTERNAL`: input=`https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf` validation=smoke status=UNKNOWN; verdict=hit; produced=3

## Catalogue notes

Extracts meta data from documents and images.

**Module ID:** `sfp_filemeta`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL, INTERESTING_FILE
**Produces:** RAW_FILE_META_DATA, SOFTWARE_USED

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `LINKED_URL_INTERNAL`
- Input: `https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf`
- Produced count: 3
