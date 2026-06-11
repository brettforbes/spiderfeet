# Yandex DNS

**Module ID:** `sfp_yandexdns`

## Summary

Check if a host would be blocked by Yandex DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://yandex.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://tech.yandex.com/, https://dns.yandex.com/advanced/

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

Yandex.DNS is a free, recursive DNS service. Yandex.DNS' servers are located in Russia, CIS countries, and Western Europe.In "Basic" mode, there is no traffic filtering. In "Safe" mode, protection from infected and fraudulent sites is provided. "Family" mode enables protection from dangerous sites and blocks sites with adult content.
