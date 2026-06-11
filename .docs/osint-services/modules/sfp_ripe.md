# RIPE

**Module ID:** `sfp_ripe`

## Summary

Queries the RIPE registry (includes ARIN data) to identify netblocks and other info.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://www.ripe.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.ripe.net/publications/ipv6-info-centre/training-and-materials, https://www.ripe.net/publications/ipv6-info-centre/ipv6-documents, https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation, https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/updating-objects-in-the-ripe-database/6-1-restful-api

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCKV6_OWNER`
- `BGP_AS_OWNER`
- `BGP_AS_MEMBER`
- **Produced:**
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCKV6_OWNER`
- `BGP_AS_MEMBER`
- `BGP_AS_OWNER`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

We're an independent, not-for-profit membership organisation that supports the infrastructure of the Internet through technical coordination in our service region. Our most prominent activity is to act as the Regional Internet Registry (RIR) providing global Internet resources and related services (IPv4, IPv6 and AS Number resources) to members in our service region.
