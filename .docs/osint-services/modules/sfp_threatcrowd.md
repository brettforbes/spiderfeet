# ThreatCrowd

**Module ID:** `sfp_threatcrowd`

## Summary

Obtain information from ThreatCrowd about identified IP addresses, domains and e-mail addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.threatcrowd.org
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://threatcrowd.blogspot.com/2015/03/tutorial.html

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `INTERNET_NAME`
- `CO_HOSTED_SITE`
- `NETBLOCK_OWNER`
- `EMAILADDR`
- `NETBLOCK_MEMBER`
- `AFFILIATE_INTERNET_NAME`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_COHOST`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`
- `MALICIOUS_EMAILADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `checkaffiliates` — Check affiliates?
- `checkcohosts` — Check co-hosted sites?
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?

## Test seeds

- `INTERNET_NAME`: input=`google.com` validation=pilot status=FINISHED; verdict=clean_miss
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

The ThreatCrowd API allows you to quickly identify related infrastructure and malware.
With the ThreatCrowd API you can search for Domains, IP Addreses, E-mail adddresses, Filehashes, Antivirus detections.
