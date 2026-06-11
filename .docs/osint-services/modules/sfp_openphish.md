# OpenPhish

**Module ID:** `sfp_openphish`

## Summary

Check if a host/domain is malicious according to OpenPhish.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://openphish.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://openphish.com/faq.html, https://openphish.com/feed.txt

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

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Timely. Accurate. Relevant Threat Intelligence.
OpenPhish is a fully automated self-contained platform for phishing intelligence. It identifies phishing sites and performs intelligence analysis in real time without human intervention and without using any external resources, such as blacklists.
