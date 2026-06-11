# ARIN

**Module ID:** `sfp_arin`

## Summary

Queries ARIN registry for contact information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://www.arin.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.arin.net/resources/, https://www.arin.net/reference/, https://www.arin.net/participate/, https://www.arin.net/resources/guide/request/, https://www.arin.net/resources/registry/transfers/, https://www.arin.net/resources/guide/ipv6/

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `HUMAN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `HUMAN_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DOMAIN_NAME`: input=`arin.net` validation=smoke status=FINISHED; verdict=hit
- `HUMAN_NAME`: input=`"ARIN Registry"` validation=pilot pilot

## Catalogue notes

ARIN is a nonprofit, member-based organization that administers IP addresses & ASNs in support of the operation and growth of the Internet.
Established in December 1997 as a Regional Internet Registry, the American Registry for Internet Numbers (ARIN) is responsible for the management and distribution of Internet number resources such as Internet Protocol (IP) addresses and Autonomous System Numbers (ASNs). ARIN manages these resources within its service region, which is comprised of Canada, the United States, and many Caribbean and North Atlantic islands.
