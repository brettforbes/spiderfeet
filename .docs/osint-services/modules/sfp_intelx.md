# IntelligenceX

**Module ID:** `sfp_intelx`

## Summary

Obtain information from IntelligenceX about identified IP addresses, domains, e-mail addresses and phone numbers.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://intelx.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ginseg.com/wp-content/uploads/sites/2/2019/07/Manual-Intelligence-X-API.pdf, https://blog.intelx.io/2019/01/25/new-developer-tab/, https://github.com/IntelligenceX/SDK

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `INTERNET_NAME`
- `EMAILADDR`
- `CO_HOSTED_SITE`
- `PHONE_NUMBER`
- `BITCOIN_ADDRESS`
- **Produced:**
- `LEAKSITE_URL`
- `DARKNET_MENTION_URL`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `EMAILADDR`
- `EMAILADDR_GENERIC`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — IntelligenceX API key.
- `base_url` — API URL, as provided in your IntelligenceX account settings.
- `checkaffiliates` — Check affiliates?
- `checkcohosts` — Check co-hosted sites?
- `maxage` — Maximum age (in days) of results to be considered valid. 0 = unlimited.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?

## Catalogue notes

Intelligence X is an independent European technology company founded in 2018 by Peter Kleissner. Its mission is to develop and maintain the search engine and data archive.
The search works with selectors, i.e. specific search terms such as email addresses, domains, URLs, IPs, CIDRs, Bitcoin addresses, IPFS hashes, etc.
It searches in places such as the darknet, document sharing platforms, whois data, public data leaks and others.
It keeps a historical data archive of results, similar to how the Wayback Machine from archive.org stores historical copies of websites.
