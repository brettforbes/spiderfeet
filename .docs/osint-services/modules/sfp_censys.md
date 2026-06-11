# Censys

**Module ID:** `sfp_censys`

## Summary

Obtain host information from Censys.io.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://censys.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://search.censys.io/api, https://search.censys.io/search/language, https://github.com/censys/censys-postman/blob/main/Censys_Search.postman_collection.json

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- **Produced:**
- `BGP_AS_MEMBER`
- `UDP_PORT_OPEN`
- `TCP_PORT_OPEN`
- `TCP_PORT_OPEN_BANNER`
- `OPERATING_SYSTEM`
- `SOFTWARE_USED`
- `WEBSERVER_HTTPHEADERS`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `GEOINFO`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `censys_api_key_secret` — Censys.io API Secret.
- `censys_api_key_uid` — Censys.io API UID.
- `delay` — Delay between requests, in seconds.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?

## Catalogue notes

Discover exposures and other common entry points for attackers.
Censys scans the entire internet constantly, including obscure ports. We use a combination of banner grabs and deep protocol handshakes to provide industry-leading visibility and an accurate depiction of what is live on the internet.
