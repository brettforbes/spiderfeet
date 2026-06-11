# Zone-H Defacement Check

**Module ID:** `sfp_zoneh`

## Summary

Check if a hostname/domain appears on the zone-h.org 'special defacements' RSS feed.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://zone-h.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.zone-h.org/archive, https://www.zone-h.org/archive/special=1

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `CO_HOSTED_SITE`
- **Produced:**
- `DEFACED_INTERNET_NAME`
- `DEFACED_IPADDR`
- `DEFACED_AFFILIATE_INTERNET_NAME`
- `DEFACED_COHOST`
- `DEFACED_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Investigate, Passive

## Module options

- `checkaffiliates` — Check affiliates?
- `checkcohosts` — Check co-hosted sites?

## Test seeds

- `INTERNET_NAME`: input=`zone-h.org` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Once a defaced website is submitted to Zone-H, it is mirrored on the Zone-H servers. The website is then moderated by the Zone-H staff to check if the defacement was fake. Sometimes, the hackers themselves submit their hacked pages to the site.
It is an Internet security portal containing original IT security news, digital warfare news, geopolitics, proprietary and general advisories, analyses, forums, researches. Zone-H is the largest web intrusions archive. It is published in several languages.
