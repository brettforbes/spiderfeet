# DNSDumpster

**Module ID:** `sfp_dnsdumpster`

## Summary

Passive subdomain enumeration using HackerTarget's DNSDumpster

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://dnsdumpster.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Investigate, Footprint, Passive

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: dnsdumpster.com removed CSRF form (2026); module needs rewrite

## Catalogue notes

DNSdumpster.com is a FREE domain research tool that can discover hosts related to a domain.
