# VirusTotal

**Module ID:** `sfp_virustotal`

## Summary

Obtain information from VirusTotal about identified IP addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.virustotal.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://developers.virustotal.com/reference

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `INTERNET_NAME`
- `CO_HOSTED_SITE`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_COHOST`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — VirusTotal API Key.
- `checkaffiliates` — Check affiliates?
- `checkcohosts` — Check co-hosted sites?
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?
- `publicapi` — Are you using a public key? If so SpiderFeet will pause for 15 seconds after each query to avoid VirusTotal dropping requests.
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Catalogue notes

Analyze suspicious files and URLs to detect types of malware, automatically share them with the security community.
