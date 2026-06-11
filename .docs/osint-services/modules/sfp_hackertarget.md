# HackerTarget

**Module ID:** `sfp_hackertarget`

## Summary

Search HackerTarget.com for hosts sharing the same IP.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://hackertarget.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://hackertarget.com/research/, https://hackertarget.com/category/tools/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- `DOMAIN_NAME_PARENT`
- **Produced:**
- `CO_HOSTED_SITE`
- `IP_ADDRESS`
- `WEBSERVER_HTTPHEADERS`
- `RAW_DNS_RECORDS`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate

## Module options

- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `http_headers` — Retrieve IP HTTP headers using HackerTarget.com
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Test seeds

- `DOMAIN_NAME_PARENT`: input=`com.au` validation=pilot pilot
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=HTTP_504; {"detail":"Scan 8D7CBA4F did not finish within 75s"}

## Catalogue notes

Simplify the security assessment process with hosted vulnerability scanners. From attack surface discovery to vulnerability identification, actionable network intelligence for IT & security operations. Proactively hunt for security weakness. Pivot from attack surface discovery to vulnerability identification.
