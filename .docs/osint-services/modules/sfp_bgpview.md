# BGPView

**Module ID:** `sfp_bgpview`

## Summary

Obtain network information from BGPView API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://bgpview.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://bgpview.docs.apiary.io/#, https://bgpview.docs.apiary.io/api-description-document

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `BGP_AS_MEMBER`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- **Produced:**
- `BGP_AS_MEMBER`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `PHYSICAL_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Test seeds

- `BGP_AS_MEMBER`: input=`15169` validation=pilot pilot
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

BGPView is a simple API allowing consumers to view all sort of analytics data about the current state and structure of the internet.
