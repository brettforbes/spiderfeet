# spur.us

**Module ID:** `sfp_spur`

## Summary

Obtain information about any malicious activities involving IP addresses found

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://spur.us/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://spur.us/api

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
- `GEOINFO`
- `COMPANY_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — spur.us API Key
- `checkaffiliates` — Check affiliates?
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?

## Catalogue notes

We expose VPNs, residential proxies, botnets, anonymization behavior, geo-fraud, and more. Anonymous infrastructure has changed; it is time the security industry caught up.
Identify commercial and private VPN exit points along with the name of the service. We expose over 80 different commercial providers.
