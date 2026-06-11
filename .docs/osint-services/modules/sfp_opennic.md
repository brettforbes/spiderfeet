# OpenNIC DNS

**Module ID:** `sfp_opennic`

## Summary

Resolves host names in the OpenNIC alternative DNS system.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.opennic.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://wiki.opennic.org/, https://servers.opennic.org

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`
- **Produced:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Investigate, Footprint, Passive

## Module options

- `checkaffiliates` — Apply checks to affiliates?

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=FINISHED; verdict=clean_miss; Benign input; expect clean_miss (negative fixture)

## Catalogue notes

An organization of hobbyists who run an alternative DNS network, also provides access to domains not administered by ICANN.
