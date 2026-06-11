# Project Honey Pot

**Module ID:** `sfp_honeypot`

## Summary

Query the Project Honey Pot database for IP addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.projecthoneypot.org/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://www.projecthoneypot.org/httpbl_api.php, https://www.projecthoneypot.org/services_overview.php, https://www.projecthoneypot.org/faq.php

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
- `BLACKLISTED_NETBLOCK`
- `BLACKLISTED_SUBNET`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — ProjectHoneyPot.org API key.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?
- `searchengine` — Include entries considered search engines?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `threatscore` — Threat score minimum, 0 being everything and 255 being only the most serious.
- `timelimit` — Maximum days old an entry can be. 255 is the maximum, 0 means you'll get nothing.

## Catalogue notes

Project Honey Pot is the first and only distributed system for identifying spammers and the spambots they use to scrape addresses from your website. Using the Project Honey Pot system you can install addresses that are custom-tagged to the time and IP address of a visitor to your site. If one of these addresses begins receiving email we not only can tell that the messages are spam, but also the exact moment when the address was harvested and the IP address that gathered it.
