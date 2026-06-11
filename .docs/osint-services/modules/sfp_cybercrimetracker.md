# CyberCrime-Tracker.net

**Module ID:** `sfp_cybercrimetracker`

## Summary

Check if a host/domain or IP address is malicious according to CyberCrime-Tracker.net.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://cybercrime-tracker.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://cybercrime-tracker.net/tools.php, https://cybercrime-tracker.net/about.php

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `CO_HOSTED_SITE`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_INTERNET_NAME`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_AFFILIATE_INTERNET_NAME`
- `BLACKLISTED_COHOST`
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
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

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

CyberCrime is a C&C panel tracker, in other words, it lists the administration interfaces of certain in-the-wild botnets.
