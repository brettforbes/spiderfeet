# ThreatFox

**Module ID:** `sfp_threatfox`

## Summary

Check if an IP address is malicious according to ThreatFox.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://threatfox.abuse.ch
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://threatfox.abuse.ch/api/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `checkaffiliates` — Apply checks to affiliates?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=error_failed; sflib:STATUS:Scan [6F7581F8] completed.; sflib:STATUS:Running 37 correlation rules on scan 6F7581F8.; sfp_threatfox:ERROR:Unexpected reply from ThreatFox: 401; sflib:STATUS:Fetched https://threatfox-api.abuse.ch/api/v1/ (25 bytes in 0.9671077728271484s); sflib:STATUS:Fetching (POST): https://threatfox-api.abuse.ch/api/v1/ (proxy=None, user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; sfp_threatfox:DEBUG:Received event, IP_ADDRESS, from SpiderFeet UI; sfp__stor_db:DEBUG:Storing an event: IP_ADDRESS; sfp__stor_db:DEBUG:Storing an event: ROOT

## Catalogue notes

ThreatFox is a free platform from abuse.ch with the goal of sharingindicators of compromise (IOCs) associated with malware with the infosec community,AV vendors and threat intelligence providers.
