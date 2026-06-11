# Pulsedive

**Module ID:** `sfp_pulsedive`

## Summary

Obtain information from Pulsedive's API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://pulsedive.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://pulsedive.com/api/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `INTERNET_NAME`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- **Produced:**
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `TCP_PORT_OPEN`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `api_key` — Pulsedive API Key.
- `checkaffiliates` — Apply checks to affiliates?
- `delay` — Delay between requests, in seconds.
- `maxnetblock` — If looking up owned netblocks, the maximum IPv4 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum IPv4 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6subnet` — If looking up subnets, the maximum IPv6 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of for blacklisting?

## Catalogue notes

Why check 30 different solutions for varying snippets of data when you can just check one? Pulsedive enriches IOCs but also fetches article summaries from Wikipedia and even posts from Reddit and the infosec blogosphere to provide contextual information for threats.
