# Google Tag Manager

**Module ID:** `sfp_google_tag_manager`

## Summary

Search Google Tag Manager (GTM) for hosts sharing the same GTM code.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://tagmanager.google.com
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://marketingplatform.google.com/about/tag-manager/, https://developers.google.com/tag-manager/quickstart, https://developers.google.com/tag-manager/devguide

## Routes

- **Route seed nugget:** `WEB_ANALYTICS_ID`
- **Consumed:**
- `WEB_ANALYTICS_ID`
- **Produced:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `AFFILIATE_INTERNET_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `verify` — Verify identified hostnames resolve to an IP address.

## Test seeds

- `WEB_ANALYTICS_ID`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

Manage all your website tags without editing code. Google Tag Manager delivers simple, reliable, easily integrated tag management solutions for free.
