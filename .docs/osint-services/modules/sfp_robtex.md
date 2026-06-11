# Robtex

**Module ID:** `sfp_robtex`

## Summary

Search Robtex.com for hosts sharing the same IP.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://www.robtex.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.robtex.com/api/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- **Produced:**
- `CO_HOSTED_SITE`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6subnet` — If looking up subnets, the maximum IPv6 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible co-hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Test seeds

- `INTERNET_NAME`: input=`8.8.8.8` validation=smoke smoke
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

Robtex is used for various kinds of research of IP numbers, Domain names, etc
Robtex uses various sources to gather public information about IP numbers, domain names, host names, Autonomous systems, routes etc. It then indexes the data in a big database and provide free access to the data.
