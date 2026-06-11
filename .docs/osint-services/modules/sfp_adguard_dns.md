# AdGuard DNS

**Module ID:** `sfp_adguard_dns`

## Summary

Check if a host would be blocked by AdGuard DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://adguard.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://adguard.com/en/adguard-dns/overview.html

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

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

AdGuard DNS is a foolproof way to block Internet ads that does not require installing any applications. It is easy to use, absolutely free, easily set up on any device, and provides you with minimal necessary functions to block ads, counters, malicious websites, and adult content.
