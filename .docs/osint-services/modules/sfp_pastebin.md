# PasteBin

**Module ID:** `sfp_pastebin`

## Summary

PasteBin search (via Google Search API) to identify related content.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://pastebin.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://pastebin.com/doc_api, https://pastebin.com/faq

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `EMAILADDR`
- **Produced:**
- `LEAKSITE_CONTENT`
- `LEAKSITE_URL`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Google API Key for PasteBin search.
- `cse_id` — Google Custom Search Engine ID.

## Catalogue notes

Pastebin is a website where you can store any text online for easy sharing. The website is mainly used by programmers to store pieces of source code or configuration information, but anyone is more than welcome to paste any type of text. The idea behind the site is to make it more convenient for people to share large amounts of text online.
