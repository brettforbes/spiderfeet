# Binary String Extractor

**Module ID:** `sfp_binstring`

## Summary

Attempt to identify strings in binary content.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_binstring
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_binstring

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- **Produced:**
- `RAW_FILE_META_DATA`

## Flags and categories

- **Flags:** errorprone
- **Categories:** Content Analysis
- **Use cases:** Footprint

## Module options

- `fileexts` — File types to fetch and analyse.
- `filterchars` — Ignore strings with these characters, as they may just be garbage ASCII.
- `maxfilesize` — Maximum file size in bytes to download for analysis.
- `maxwords` — Stop reporting strings from a single binary after this many are found.
- `minwordsize` — Upon finding a string in a binary, ensure it is at least this length. Helps weed out false positives.
- `usedict` — Use the dictionary to further reduce false positives - any string found must contain a word from the dictionary (can be very slow, especially for larger files).

## Test seeds

- `LINKED_URL_INTERNAL`: input=`https://www.google.com/favicon.ico` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Attempt to identify strings in binary content.

**Module ID:** `sfp_binstring`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL
**Produces:** RAW_FILE_META_DATA
**Flags:** errorprone

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `LINKED_URL_INTERNAL`
- Input: `https://example.com/binary`
- Produced count: 0
