# DNS Raw Records

**Module ID:** `sfp_dnsraw`

## Summary

Retrieves raw DNS records such as MX, TXT and others.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_dnsraw
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnsraw

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `DOMAIN_NAME_PARENT`
- **Produced:**
- `PROVIDER_MAIL`
- `PROVIDER_DNS`
- `RAW_DNS_RECORDS`
- `DNS_TEXT`
- `DNS_SPF`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `verify` — Verify identified hostnames resolve.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=10

## Catalogue notes

Retrieves raw DNS records such as MX, TXT and others.

**Module ID:** `sfp_dnsraw`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, DOMAIN_NAME, DOMAIN_NAME_PARENT
**Produces:** PROVIDER_MAIL, PROVIDER_DNS, RAW_DNS_RECORDS, DNS_TEXT, DNS_SPF, INTERNET_NAME, INTERNET_NAME_UNRESOLVED, AFFILIATE_INTERNET_NAME…

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 10
