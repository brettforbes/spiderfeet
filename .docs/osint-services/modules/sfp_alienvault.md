# AlienVault OTX

**Module ID:** `sfp_alienvault`

## Summary

Obtain information from AlienVault Open Threat Exchange (OTX)

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://otx.alienvault.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://otx.alienvault.com/faq, https://otx.alienvault.com/api, https://otx.alienvault.com/submissions/list, https://otx.alienvault.com/pulse/create, https://otx.alienvault.com/endpoint-security/welcome, https://otx.alienvault.com/browse/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `CO_HOSTED_SITE`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `LINKED_URL_INTERNAL`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — AlienVault OTX API Key.
- `checkaffiliates` — Apply checks to affiliates?
- `cohost_age_limit_days` — Ignore any co-hosts older than this many days. 0 = unlimited.
- `max_pages` — Maximum number of pages of URL results to fetch.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum IPv4 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum IPv4 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — If looking up owned netblocks, the maximum IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6subnet` — If looking up subnets, the maximum IPv6 subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `reputation_age_limit_days` — Ignore any reputation records older than this many days. 0 = unlimited.
- `subnetlookup` — Look up all IPs on subnets which your target is a part of for blacklisting?
- `threat_score_min` — Minimum AlienVault threat score.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

The World’s First Truly Open Threat Intelligence Community
Open Threat Exchange is the neighborhood watch of the global intelligence community. It enables private companies, independent security researchers, and government agencies to openly collaborate and share the latest information about emerging threats, attack methods, and malicious actors, promoting greater security across the entire community.
OTX changed the way the intelligence community creates and consumes threat data. In OTX, anyone in the security community can contribute, discuss, research, validate, and share threat data. You can integrate community-generated OTX threat data directly into your AlienVault and third-party security products, so that your threat detection defenses are always up to date with the latest threat intelligence. Today, 100,000 participants in 140 countries contribute over 19 million threat indicators daily.
