# Flickr

**Module ID:** `sfp_flickr`

## Summary

Search Flickr for domains, URLs and emails related to the specified domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** https://www.flickr.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.flickr.com/services/api/, https://www.flickr.com/services/developer/api/, https://code.flickr.net/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `LINKED_URL_INTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `dns_resolve` — DNS resolve each identified domain.
- `maxpages` — Maximum number of pages of results to fetch.
- `pause` — Number of seconds to pause between fetches.
- `per_page` — Maximum number of results per page.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: Flickr API key scrape fails (Failed to obtain API key); needs API key config

## Catalogue notes

Flickr is almost certainly the best online photo management and sharing application in the world.
 On Flickr, members upload photos, share them securely, supplement their photos with metadata like license information, geo-location, people, tags, etc., and interact with their family, friends, contacts or anyone in the community. Practically all the features on Flickr's various platforms -- web, mobile and desktop -- are accompanied by a longstanding API program. Since 2005, developers have collaborated on top of Flickr's APIs to build fun, creative, and gorgeous experiences around photos that extend beyond Flickr.
