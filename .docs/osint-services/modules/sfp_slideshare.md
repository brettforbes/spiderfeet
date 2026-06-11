# SlideShare

**Module ID:** `sfp_slideshare`

## Summary

Gather name and location from SlideShare profiles.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.slideshare.net
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.slideshare.net/developers/documentation, https://www.slideshare.net/developers, https://www.slideshare.net/developers/resources, https://www.slideshare.net/developers/oembed

## Routes

- **Route seed nugget:** `SOCIAL_MEDIA`
- **Consumed:**
- `SOCIAL_MEDIA`
- **Produced:**
- `RAW_RIR_DATA`
- `GEOINFO`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `SOCIAL_MEDIA`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

LinkedIn SlideShare is an American hosting service for professional content including presentations, infographics, documents, and videos. Users can upload files privately or publicly in PowerPoint, Word, PDF, or OpenDocument format.
