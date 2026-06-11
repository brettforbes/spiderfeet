# Maltiverse

**Module ID:** `sfp_maltiverse`

## Summary

Obtain information about any malicious activities involving IP addresses

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://maltiverse.com
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://maltiverse.com/faq, https://app.swaggerhub.com/apis-docs/maltiverse/api/1.0.0-oas3

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- `AFFILIATE_IPADDR`
- **Produced:**
- `IP_ADDRESS`
- `MALICIOUS_IPADDR`
- `RAW_RIR_DATA`
- `MALICIOUS_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `checkaffiliates` — Check affiliates?
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

The Open IOC Search Engine.
Enhance your SIEM or Firewall and crosscheck your event data with top quality Threat Intelligence information to highlight what requires action.
