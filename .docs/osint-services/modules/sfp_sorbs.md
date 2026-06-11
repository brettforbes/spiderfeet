# SORBS

**Module ID:** `sfp_sorbs`

## Summary

Query the SORBS database for open relays, open proxies, vulnerable servers, etc.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://www.sorbs.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** http://www.sorbs.net/information/proxy.shtml, http://www.sorbs.net/information/spamfo/, http://www.sorbs.net/general/using.shtml

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
- `PROXY_HOST`

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

The Spam and Open Relay Blocking System (SORBS) was conceived as an anti-spam project where a daemon would check "on-the-fly", all servers from which it received email to determine if that email was sent via various types of proxy and open-relay servers.
The SORBS (Spam and Open Relay Blocking System) provides free access to its DNS-based Block List (DNSBL) to effectively block email from more than 12 million host servers known to disseminate spam, phishing attacks and other forms of malicious email.
