# Psbdmp

**Module ID:** `sfp_psbdmp`

## Summary

Check psbdmp.cc (PasteBin Dump) for potentially hacked e-mails and domains.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://psbdmp.cc/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://psbdmp.cc/api

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `EMAILADDR`
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `LEAKSITE_URL`
- `LEAKSITE_CONTENT`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `EMAILADDR`: input=`noreply@spiderfoot.net` validation=smoke status=FINISHED; verdict=error_failed; sflib:STATUS:Running 37 correlation rules on scan C73F8DA0.; sfp_psbdmp:ERROR:Error processing JSON response from psbdmp.cc: Expecting value: line 1 column 1 (char 0); sflib:STATUS:Fetched https://psbdmp.cc/api/search/email/noreply@spiderfoot.net (146 bytes in 0.6718180179595947s); sfp_psbdmp:DEBUG:Received event, EMAILADDR, from SpiderFeet UI; sflib:STATUS:Fetching (GET): https://psbdmp.cc/api/search/email/noreply@spiderfoot.net (proxy=None, user-agent=SpiderFeet, timeout=15; sfp__stor_db:DEBUG:Storing an event: EMAILADDR; sfp__stor_db:DEBUG:Storing an event: ROOT; sflib:STATUS:sfp_psbdmp module loaded.
- `INTERNET_NAME`: input=`noreply@spiderfoot.net` validation=smoke status=FINISHED; verdict=error_failed; sflib:STATUS:Running 37 correlation rules on scan C73F8DA0.; sfp_psbdmp:ERROR:Error processing JSON response from psbdmp.cc: Expecting value: line 1 column 1 (char 0); sflib:STATUS:Fetched https://psbdmp.cc/api/search/email/noreply@spiderfoot.net (146 bytes in 0.6718180179595947s); sfp_psbdmp:DEBUG:Received event, EMAILADDR, from SpiderFeet UI; sflib:STATUS:Fetching (GET): https://psbdmp.cc/api/search/email/noreply@spiderfoot.net (proxy=None, user-agent=SpiderFeet, timeout=15; sfp__stor_db:DEBUG:Storing an event: EMAILADDR; sfp__stor_db:DEBUG:Storing an event: ROOT; sflib:STATUS:sfp_psbdmp module loaded.
