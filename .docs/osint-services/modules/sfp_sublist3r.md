# Sublist3r PassiveDNS

**Module ID:** `sfp_sublist3r`

## Summary

Passive subdomain enumeration using Sublist3r's API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://api.sublist3r.com
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

- `DOMAIN_NAME`: input=`sbs.com.au` validation=blocked-upstream SPEC_GAP upstream: api.sublist3r.com returns empty/non-JSON body
