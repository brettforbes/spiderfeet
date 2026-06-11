# Fraudguard

**Module ID:** `sfp_fraudguard`

## Summary

Obtain threat information from Fraudguard.io

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://fraudguard.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.fraudguard.io/, https://faq.fraudguard.io/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- **Produced:**
- `GEOINFO`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_SUBNET`
- `MALICIOUS_NETBLOCK`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `checkaffiliates` — Apply checks to affiliates?
- `fraudguard_api_key_account` — Fraudguard.io API username.
- `fraudguard_api_key_password` — Fraudguard.io API password.
- `maxnetblock` — If looking up owned netblocks, the maximum IPv4 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum IPv4 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6subnet` — If looking up subnets, the maximum IPv6 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of for blacklisting?

## Catalogue notes

FraudGuard is a service designed to provide an easy way to validate usage by continuously collecting and analyzing real-time internet traffic. Utilizing just a few simple API endpoints we make integration as simple as possible and return data such as: Risk Level, Threat Type, Geo Location, etc. Super fast, super simple.
Lookup any IP address by querying our threat engine.
