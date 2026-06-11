# DNS Resolver

**Module ID:** `sfp_dnsresolve`

## Summary

Resolves hosts and IP addresses identified, also extracted from raw content.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_dnsresolve
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnsresolve

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `CO_HOSTED_SITE`
- `AFFILIATE_INTERNET_NAME`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `TARGET_WEB_CONTENT`
- `BASE64_DATA`
- `AFFILIATE_DOMAIN_WHOIS`
- `CO_HOSTED_SITE_DOMAIN_WHOIS`
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `LEAKSITE_CONTENT`
- `RAW_DNS_RECORDS`
- `RAW_FILE_META_DATA`
- `RAW_RIR_DATA`
- `SIMILARDOMAIN_WHOIS`
- `SSL_CERTIFICATE_RAW`
- `SSL_CERTIFICATE_ISSUED`
- `TCP_PORT_OPEN_BANNER`
- `WEBSERVER_BANNER`
- `WEBSERVER_HTTPHEADERS`
- **Produced:**
- `IP_ADDRESS`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `DOMAIN_NAME`
- `IPV6_ADDRESS`
- `INTERNAL_IP_ADDRESS`
- `DOMAIN_NAME_PARENT`
- `CO_HOSTED_SITE_DOMAIN`
- `AFFILIATE_DOMAIN_NAME`
- `INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `maxnetblock` — Maximum owned IPv4 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxv6netblock` — Maximum owned IPv6 netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?
- `skipcommononwildcard` — If wildcard DNS is detected, only attempt to look up the first common sub-domain from the common sub-domain list.
- `validatereverse` — Validate that reverse-resolved hostnames still resolve back to that IP before considering them as aliases of your target.

## Test seeds

- `INTERNET_NAME`: input=`one.one.one.one` validation=smoke status=UNKNOWN; verdict=hit; produced=5

## Catalogue notes

Resolves hosts and IP addresses identified, also extracted from raw content.

**Module ID:** `sfp_dnsresolve`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** CO_HOSTED_SITE, AFFILIATE_INTERNET_NAME, NETBLOCK_OWNER, NETBLOCKV6_OWNER, IP_ADDRESS, IPV6_ADDRESS, INTERNET_NAME, AFFILIATE_IPADDR…
**Produces:** IP_ADDRESS, INTERNET_NAME, AFFILIATE_INTERNET_NAME, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS, DOMAIN_NAME, IPV6_ADDRESS, INTERNAL_IP_ADDRESS…

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `INTERNET_NAME`
- Input: `one.one.one.one`
- Produced count: 5
