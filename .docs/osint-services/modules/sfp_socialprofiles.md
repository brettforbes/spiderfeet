# Social Media Profile Finder

**Module ID:** `sfp_socialprofiles`

## Summary

Tries to discover the social media profiles for human names identified.

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

- **Route seed nugget:** `HUMAN_NAME`
- **Consumed:**
- `HUMAN_NAME`
- **Produced:**
- `SOCIAL_MEDIA`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** slow, apikey
- **Categories:** Social Media
- **Use cases:** Footprint, Passive

## Module options

- `bing_api_key` — Bing API Key for social media profile search.
- `count` — Number of bing search engine results of identified profiles to iterate through.
- `google_api_key` — Google API Key for social media profile search.
- `google_cse_id` — Google Custom Search Engine ID.
- `method` — Search engine to use: 'google' or 'bing'.
- `tighten` — Tighten results by expecting to find the keyword of the target domain mentioned in the social media profile page results?

## Catalogue notes

Google Custom Search enables you to create a search engine for your website, your blog, or a collection of websites. You can configure your engine to search both web pages and images. You can fine-tune the ranking, add your own promotions and customize the look and feel of the search results. You can monetize the search by connecting your engine to your Google AdSense account.
