# Keybase

**Module ID:** `sfp_keybase`

## Summary

Obtain additional information about domain names and identified usernames.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://keybase.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://keybase.io/docs/api/1.0/call/user/lookup

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `USERNAME`
- `LINKED_URL_EXTERNAL`
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `SOCIAL_MEDIA`
- `USERNAME`
- `GEOINFO`
- `BITCOIN_ADDRESS`
- `PGP_KEY`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DOMAIN_NAME`: input=`spiderfeet` validation=smoke status=FINISHED; verdict=clean_miss; Finalize: benign input clean_miss (negative fixture)
- `USERNAME`: input=`spiderfeet` validation=smoke status=FINISHED; verdict=clean_miss; Finalize: benign input clean_miss (negative fixture)

## Catalogue notes

Keybase is a key directory that maps social media identities to encryption keys in a publicly auditable manner.
