# grep.app

**Module ID:** `sfp_grep_app`

## Summary

Search grep.app API for links and emails related to the specified domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://grep.app/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `RAW_RIR_DATA`
- `INTERNET_NAME_UNRESOLVED`
- `LINKED_URL_INTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `dns_resolve` — DNS resolve each identified domain.
- `max_pages` — Maximum number of pages of results to fetch.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

grep.app searches code from over a half million public repositories on GitHub.
It searches for the exact string you enter, including any punctuation or other characters.
You can also search by regular expression, using the RE2 syntax.
