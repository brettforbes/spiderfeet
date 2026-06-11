# CloudFlare DNS

**Module ID:** `sfp_cloudflaredns`

## Summary

Check if a host would be blocked by CloudFlare DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.cloudflare.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://developers.cloudflare.com/1.1.1.1/1.1.1.1-for-families/

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

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

1.1.1.1 for Families is the easiest way to add a layer of protection to your home network and protect it from malware and adult content. 1.1.1.1 for Families leverages Cloudflare’s global network to ensure that it is fast and secure around the world.
