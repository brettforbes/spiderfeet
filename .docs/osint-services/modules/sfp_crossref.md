# Cross-Referencer

**Module ID:** `sfp_crossref`

## Summary

Identify whether other domains are associated ('Affiliates') of the target by looking for links back to the target site(s).

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_crossref
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_crossref

## Routes

- **Route seed nugget:** `LINKED_URL_EXTERNAL`
- **Consumed:**
- `LINKED_URL_EXTERNAL`
- `SIMILARDOMAIN`
- `CO_HOSTED_SITE`
- `DARKNET_MENTION_URL`
- **Produced:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_WEB_CONTENT`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint

## Module options

- `checkbase` — Check the base URL of the potential affiliate if no direct affiliation found?

## Test seeds

- `LINKED_URL_EXTERNAL`: input=`https://www.iana.org/help/example-domains` validation=smoke status=UNKNOWN; verdict=hit; produced=2

## Catalogue notes

Identify whether other domains are associated ('Affiliates') of the target by looking for links back to the target site(s).

**Module ID:** `sfp_crossref`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_EXTERNAL, SIMILARDOMAIN, CO_HOSTED_SITE, DARKNET_MENTION_URL
**Produces:** AFFILIATE_INTERNET_NAME, AFFILIATE_WEB_CONTENT

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
