# DNS Zone Transfer

**Module ID:** `sfp_dnszonexfer`

## Summary

Attempts to perform a full DNS zone transfer.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_dnszonexfer
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnszonexfer

## Routes

- **Route seed nugget:** `PROVIDER_DNS`
- **Consumed:**
- `PROVIDER_DNS`
- **Produced:**
- `RAW_DNS_RECORDS`
- `INTERNET_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Module options

- `timeout` — Timeout in seconds

## Test seeds

- `PROVIDER_DNS`: input=`8.8.8.8` validation=smoke status=UNKNOWN; verdict=clean_miss; produced=0

## Catalogue notes

Attempts to perform a full DNS zone transfer.

**Module ID:** `sfp_dnszonexfer`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** PROVIDER_DNS
**Produces:** RAW_DNS_RECORDS, INTERNET_NAME

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 0
