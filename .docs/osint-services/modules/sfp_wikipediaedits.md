# Wikipedia Edits

**Module ID:** `sfp_wikipediaedits`

## Summary

Identify edits to Wikipedia articles made from a given IP address or username.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.wikipedia.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.mediawiki.org/wiki/API:Tutorial, https://www.mediawiki.org/wiki/How_to_contribute, https://www.mediawiki.org/wiki/API:Main_page

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `USERNAME`
- **Produced:**
- `WIKIPEDIA_PAGE_EDIT`

## Flags and categories

- **Flags:** —
- **Categories:** Secondary Networks
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `days_limit` — Maximum age of data to be considered valid (0 = unlimited).

## Test seeds

- `IP_ADDRESS`: input=`91.198.174.192` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Wikipedia is a multilingual online encyclopedia created and maintained as an open collaboration project by a community of volunteer editors, using a wiki-based editing system.
