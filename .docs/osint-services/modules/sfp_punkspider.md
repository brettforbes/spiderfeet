# PunkSpider

**Module ID:** `sfp_punkspider`

## Summary

Check the QOMPLX punkspider.io service to see if the target is listed as vulnerable.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://punkspider.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `VULNERABILITY_GENERAL`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

The idea behind Punkspider is very simple - we're doing a bunch of complicated stuff to find insecurities in massive amounts of websites, with the goal of scanning the entire Internet.
