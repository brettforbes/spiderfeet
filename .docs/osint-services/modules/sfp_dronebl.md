# DroneBL

**Module ID:** `sfp_dronebl`

## Summary

Query the DroneBL database for open relays, open proxies, vulnerable servers, etc.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://dronebl.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://dronebl.org/docs/howtouse, https://dronebl.org/rpckey_signup, https://dronebl.org/docs/rpc2

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
- `VPN_HOST`
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

DroneBL is a realtime monitor of abusable IPs, which has the goal of stopping abuse of infected machines.
A real-time tracker of abusable IPs.
