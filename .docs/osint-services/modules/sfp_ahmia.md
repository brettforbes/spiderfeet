# Ahmia

**Module ID:** `sfp_ahmia`

## Summary

Search Tor 'Ahmia' search engine for mentions of the target.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://ahmia.fi/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://ahmia.fi/documentation/, https://github.com/ahmia/, http://msydqstlz2kzerdg.onion/, https://ahmia.fi/stats

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

- **Flags:** tor
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate

## Module options

- `fetchlinks` — Fetch the darknet pages (via TOR, if enabled) to verify they mention your target.
- `fullnames` — Search for human names?

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

Ahmia searches hidden services on the Tor network. To access these hidden services,you need the Tor browser bundle. Abuse material is not allowed on Ahmia. See our service blacklist and report abuse material if you find it in the index. It will be removed as soon as possible.
Contributors to Ahmia believe that the Tor network is an important and resilient distributed platform for anonymity and privacy worldwide. By providing a search engine for what many call the "deep web" or "dark net", Ahmia makes hidden services accessible to a wide range of people, not just Tor network early adopters.
