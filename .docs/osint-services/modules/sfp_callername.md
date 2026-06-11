# CallerName

**Module ID:** `sfp_callername`

## Summary

Lookup US phone number location and reputation information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://callername.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://callername.com/faq, https://callername.com/stats

## Routes

- **Route seed nugget:** `PHONE_NUMBER`
- **Consumed:**
- `PHONE_NUMBER`
- **Produced:**
- `GEOINFO`
- `MALICIOUS_PHONE_NUMBER`

## Flags and categories

- **Flags:** —
- **Categories:** Real World
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `PHONE_NUMBER`: input=`+18005551212` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

CallerName is a free, reverse phone lookup service for both cell and landline numbers. It relies on a database of white pages and business pages taken from public sources. The easy-to-use and streamlined interface allow users to look up the caller ID information of any number quickly. Just type the unknown number into the search bar to start. You need not pay nor register to use this 100% free service.
