# multiproxy.org Open Proxies

**Module ID:** `sfp_multiproxy`

## Summary

Check if an IP address is an open proxy according to multiproxy.org open proxy list.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://multiproxy.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://multiproxy.org/faq.htm, https://multiproxy.org/env_check.htm, https://multiproxy.org/anon_proxy.htm, https://multiproxy.org/help.htm

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

## Flags and categories

- **Flags:** —
- **Categories:** Secondary Networks
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

MultiProxy is a multifunctional personal proxy server that protects your privacy while on the Internet as well as speeds up your downloads, especially if you are trying to get several files form overseas or from otherwise rather slow server. It can also completely hide your IP address by dynamically connecting to non-transparent anonymizing public proxy servers. You can also test a list of proxy servers and sort them by connection speed and level of anonimity.
