# XForce Exchange

**Module ID:** `sfp_xforce`

## Summary

Obtain IP reputation and passive DNS information from IBM X-Force Exchange.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://exchange.xforce.ibmcloud.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://api.xforce.ibmcloud.com/doc/, https://exchange.xforce.ibmcloud.com/faq

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `IPV6_ADDRESS`
- `AFFILIATE_IPV6_ADDRESS`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_SUBNET`
- `BLACKLISTED_NETBLOCK`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`
- `CO_HOSTED_SITE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `checkaffiliates` — Apply checks to affiliates?
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6subnet` — If looking up subnets, the maximum IPv6 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of for blacklisting?
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.
- `xforce_api_key` — X-Force Exchange API Key.
- `xforce_api_key_password` — X-Force Exchange API Password.

## Catalogue notes

IBM® X-Force Exchange is a cloud-based, threat intelligence sharing platform that you can use to rapidly research the latest global security threats, aggregate actionable intelligence, consult with experts and collaborate with peers. IBM X-Force Exchange, supported by human- and machine-generated intelligence, leverages the scale of IBM X-Force to help users stay ahead of emerging threats.
