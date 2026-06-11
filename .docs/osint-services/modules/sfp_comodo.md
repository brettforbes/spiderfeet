# Comodo Secure DNS

**Module ID:** `sfp_comodo`

## Summary

Check if a host would be blocked by Comodo Secure DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.comodo.com/secure-dns/
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** https://cdome.comodo.com/pdf/Datasheet-Dome-Shield.pdf, http://securedns.dnsbycomodo.com/, https://www.comodo.com/secure-dns/secure-dns-assets/dowloads/ccs-dome-shield-whitepaper-threat-intelligence.pdf, https://www.comodo.com/secure-dns/secure-dns-assets/dowloads/domeshield-all-use-cases.pdf

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

Comodo Secure DNS is a domain name resolution service that resolves your DNS requests through our worldwide network of redundant DNS servers, bringing you the most reliable fully redundant DNS service anywhere, for a safer, smarter and faster Internet experience.
