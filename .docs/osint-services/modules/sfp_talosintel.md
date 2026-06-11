# Talos Intelligence

**Module ID:** `sfp_talosintel`

## Summary

Check if a netblock or IP address is malicious according to TalosIntelligence.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://talosintelligence.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://talosintelligence.com/vulnerability_info, https://talosintelligence.com/reputation

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

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=error_failed; sflib:STATUS:Scan [300AE55A] completed.; sflib:STATUS:Running 37 correlation rules on scan 300AE55A.; sfp_talosintel:ERROR:Unexpected HTTP response code 403 from Talos Intelligence.; sflib:STATUS:Fetched https://snort.org/downloads/ip-block-list (5690 bytes in 0.11820507049560547s); sflib:STATUS:Fetching (GET): https://snort.org/downloads/ip-block-list (proxy=None, user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x; sfp_talosintel:DEBUG:Received event, IP_ADDRESS, from SpiderFeet UI; sfp_talosintel:DEBUG:Checking maliciousness of 8.8.8.8 (IP_ADDRESS) with Talos Intelligence; sfp__stor_db:DEBUG:Storing an event: IP_ADDRESS

## Catalogue notes

Cisco Talos Incident Response provides a full suite of proactive and reactive services to help you prepare, respond and recover from a breach. With Talos IR, you have direct access to the same threat intelligence available to Cisco and world-class emergency response capabilities — in addition to more than 350 threat researchers for questions and analysis. Let our experts work with you to evaluate existing plans, develop a new plan, and provide rapid assistance when you need it most.
