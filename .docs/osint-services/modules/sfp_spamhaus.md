# Spamhaus Zen

**Module ID:** `sfp_spamhaus`

## Summary

Check if a netblock or IP address is in the Spamhaus Zen database.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.spamhaus.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.spamhaus.org/zen/, https://www.spamhaus.org/organization/dnsblusage/, https://www.spamhaus.org/datafeed/, https://www.spamhaus.org/whitepapers/dnsbl_function/, https://www.spamhaus.org/faq/section/DNSBL%20Usage

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_SUBNET`
- `BLACKLISTED_NETBLOCK`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of for blacklisting?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

The Spamhaus Project is an international nonprofit organization that tracks spam and related cyber threats such as phishing, malware and botnets, provides realtime actionable and highly accurate threat intelligence to the Internet's major networks, corporations and security vendors, and works with law enforcement agencies to identify and pursue spam and malware sources worldwide. ZEN is the combination of all Spamhaus IP-based DNSBLs into one single powerful and comprehensive blocklist to make querying faster and simpler. It contains the SBL, SBLCSS, XBL and PBL blocklists.
