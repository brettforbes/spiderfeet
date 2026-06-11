# Google

**Module ID:** `sfp_googlesearch`

## Summary

Obtain information from the Google Custom Search API to identify sub-domains and links.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://developers.google.com/custom-search
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://developers.google.com/custom-search/v1, https://developers.google.com/custom-search/docs/overview, https://cse.google.com/cse

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `LINKED_URL_INTERNAL`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Google API Key for Google search.
- `cse_id` — Google Custom Search Engine ID.

## Catalogue notes

Google Custom Search enables you to create a search engine for your website, your blog, or a collection of websites. You can configure your engine to search both web pages and images. You can fine-tune the ranking, add your own promotions and customize the look and feel of the search results. You can monetize the search by connecting your engine to your Google AdSense account.
