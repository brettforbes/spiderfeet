# blocklist.de

**Module ID:** `sfp_blocklistde`

## Summary

Check if a netblock or IP is malicious according to blocklist.de.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://www.blocklist.de/en/index.html
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** http://www.blocklist.de/en/api.html, http://www.blocklist.de/en/rbldns.html, http://www.blocklist.de/en/httpreports.html, http://www.blocklist.de/en/export.html, http://www.blocklist.de/en/delist.html?ip=

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `NETBLOCK_MEMBER`
- `NETBLOCKV6_MEMBER`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
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
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

www.blocklist.de is a free and voluntary service provided by a Fraud/Abuse-specialist, whose servers are often attacked via SSH-, Mail-Login-, FTP-, Webserver- and other services.
The mission is to report any and all attacks to the respective abuse departments of the infected PCs/servers, to ensure that the responsible provider can inform their customer about the infection and disable the attacker.
