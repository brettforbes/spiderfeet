# Hash Extractor

**Module ID:** `sfp_hashes`

## Summary

Identify MD5 and SHA hashes in web content, files and more.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_hashes
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_hashes

## Routes

- **Route seed nugget:** `BASE64_DATA`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `BASE64_DATA`
- `LEAKSITE_CONTENT`
- `RAW_DNS_RECORDS`
- `RAW_FILE_META_DATA`
- **Produced:**
- `HASH`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `BASE64_DATA`: input=`5d41402abc4b2a76b9719d911017c592 (md5)` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify MD5 and SHA hashes in web content, files and more.

**Module ID:** `sfp_hashes`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, BASE64_DATA, LEAKSITE_CONTENT, RAW_DNS_RECORDS, RAW_FILE_META_DATA
**Produces:** HASH

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `BASE64_DATA`
- Input: `5d41402abc4b2a76b9719d911017c592 (md5)`
- Produced count: 1
