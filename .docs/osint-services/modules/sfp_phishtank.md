# PhishTank

**Module ID:** `sfp_phishtank`

## Summary

Check if a host/domain is malicious according to PhishTank.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://phishtank.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://phishtank.com/developer_info.php

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `CO_HOSTED_SITE`
- **Produced:**
- `BLACKLISTED_INTERNET_NAME`
- `BLACKLISTED_AFFILIATE_INTERNET_NAME`
- `BLACKLISTED_COHOST`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_COHOST`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checkcohosts` — Apply checks to sites found to be co-hosted on the target's IP?

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=error_failed; sfp_phishtank:ERROR:Unexpected HTTP response code 429 from phishtank.com.; sflib:STATUS:Fetched https://data.phishtank.com/data/online-valid.csv (236 bytes in 0.8407688140869141s); sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNET_NAME; sfp__stor_db:DEBUG:Storing an event: ROOT; sflib:STATUS:Fetching (GET): https://data.phishtank.com/data/online-valid.csv (proxy=None, user-agent=SpiderFeet, timeout=5, cookies=; sfp_phishtank:DEBUG:Received event, INTERNET_NAME, from SpiderFeet UI; sfp_phishtank:DEBUG:Checking maliciousness of sbs.com.au (INTERNET_NAME) with phishtank.com

## Catalogue notes

Submit suspected phishes. Track the status of your submissions. Verify other users' submissions.
