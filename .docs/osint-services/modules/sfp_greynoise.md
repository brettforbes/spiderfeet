# GreyNoise

**Module ID:** `sfp_greynoise`

## Summary

Obtain IP enrichment data from GreyNoise

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://greynoise.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.greynoise.io/, https://viz.greynoise.io/signup

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_ASN`
- `MALICIOUS_SUBNET`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `COMPANY_NAME`
- `GEOINFO`
- `BGP_AS_MEMBER`
- `OPERATING_SYSTEM`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `api_key` — GreyNoise API Key.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up subnets which your target is a part of for blacklisting?

## Catalogue notes

At GreyNoise, we collect and analyze untargeted, widespread, and opportunistic scan and attack activity that reaches every server directly connected to the Internet. Mass scanners (such as Shodan and Censys), search engines, bots, worms, and crawlers generate logs and events omnidirectionally on every IP address in the IPv4 space. GreyNoise gives you the ability to filter this useless noise out.
