# TORCH

**Module ID:** `sfp_torch`

## Summary

Search Tor 'TORCH' search engine for mentions of the target domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://torchsearch.wordpress.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `HUMAN_NAME`
- `EMAILADDR`
- **Produced:**
- `DARKNET_MENTION_URL`
- `DARKNET_MENTION_CONTENT`

## Flags and categories

- **Flags:** errorprone, tor
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate

## Module options

- `fetchlinks` — Fetch the darknet pages (via TOR, if enabled) to verify they mention your target.
- `fullnames` — Search for human names?
- `pages` — Number of results pages to iterate through.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

Torch or TorSearch is the best search engine for the hidden part of the internet. They're also the oldest and longest running search engine on Tor.
Torch claims to have over one billion dark net pages indexed. They also don't censor search results or track what you search for.
