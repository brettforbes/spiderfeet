# CoinBlocker Lists

**Module ID:** `sfp_coinblocker`

## Summary

Check if a domain appears on CoinBlocker lists.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://zerodot1.gitlab.io/CoinBlockerListsWeb/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://zerodot1.gitlab.io/CoinBlockerListsWeb/downloads.html, https://zerodot1.gitlab.io/CoinBlockerListsWeb/references.html, https://zerodot1.gitlab.io/CoinBlockerListsWeb/aboutthisproject.html

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

The CoinBlockerLists are a project to prevent illegal mining in browsers or other applications using IPlists and URLLists.
It's not just to block everything without any reason, but to protect Internet users from illegal mining.
