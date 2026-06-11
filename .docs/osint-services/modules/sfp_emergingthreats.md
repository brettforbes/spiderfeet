# Emerging Threats

**Module ID:** `sfp_emergingthreats`

## Summary

Check if a netblock or IP address is malicious according to EmergingThreats.net.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://rules.emergingthreats.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://doc.emergingthreats.net/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_SUBNET`
- `BLACKLISTED_NETBLOCK`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_SUBNET`
- `MALICIOUS_NETBLOCK`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliate IP addresses?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Emerging Threats delivers the most timely and accurate threat intelligence.
Emerging Threat (ET) intelligence helps prevent attacks and reduce risk by helping you understand the historical context of where these threats originated, who is behind them, when have they attacked, what methods they used, and what they're after. Get on-demand access to current and historical metadata on IPs, domains, and other related threat intelligence to help research threats and investigate incidents.
