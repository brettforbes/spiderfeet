# Quad9

**Module ID:** `sfp_quad9`

## Summary

Check if a host would be blocked by Quad9 DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://quad9.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.quad9.net/faq/, https://support.quad9.net/hc/en-us/categories/360002571772-Configuration

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

Quad9 brings together cyber threat intelligence about malicious domains from a variety of public and private sources and blocks access to those malicious domains when your system attempts to contact them.
When you use Quad9, attackers and malware cannot leverage the known malicious domains to control your systems, and their ability to steal your data or cause harm will be hindered. Quad9 is an effective and easy way to add an additional layer of security to your infrastructure for free.
