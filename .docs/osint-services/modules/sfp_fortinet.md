# FortiGuard Antispam

**Module ID:** `sfp_fortinet`

## Summary

Check if an IP address is malicious according to FortiGuard Antispam.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.fortiguard.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.fortiguard.com/learnmore#as

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `checkaffiliates` — Apply checks to affiliates?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

FortiGuard Antispam provides a comprehensive and multi-layered approach to detect and filter spam processed by organizations.
