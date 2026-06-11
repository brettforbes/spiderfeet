# VoIP Blacklist (VoIPBL)

**Module ID:** `sfp_voipbl`

## Summary

Check if an IP address or netblock is malicious according to VoIP Blacklist (VoIPBL).

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://voipbl.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://voipbl.org/#install, https://voipbl.org/#advanced

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
- `checkaffiliates` — Apply checks to affiliates?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

VoIPBL is a distributed VoIP blacklist that is aimed to protect against
VoIP Fraud and minimizing abuse for network that have publicly accessible PBXs.
