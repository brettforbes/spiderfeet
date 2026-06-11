# Gravatar

**Module ID:** `sfp_gravatar`

## Summary

Retrieve user information from Gravatar API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://secure.gravatar.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://secure.gravatar.com/site/implement/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `RAW_RIR_DATA`
- `USERNAME`
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `PHONE_NUMBER`
- `GEOINFO`
- `ACCOUNT_EXTERNAL_OWNED`
- `SOCIAL_MEDIA`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `EMAILADDR`: input=`noreply@example.com` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

Your Gravatar is an image that follows you from site to site appearing beside your name when you do things like comment or post on a blog.
A Gravatar is a Globally Recognized Avatar. You upload it and create your profile just once, and then when you participate in any Gravatar-enabled site, your Gravatar image will automatically follow you there.
