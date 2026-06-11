# JsonWHOIS.com

**Module ID:** `sfp_jsonwhoiscom`

## Summary

Search JsonWHOIS.com for WHOIS records associated with a domain.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://jsonwhois.com
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://jsonwhois.com/docs

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `DOMAIN_REGISTRAR`
- `DOMAIN_WHOIS`
- `PROVIDER_DNS`
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `PHONE_NUMBER`
- `PHYSICAL_ADDRESS`
- `AFFILIATE_DOMAIN_UNREGISTERED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — JsonWHOIS.com API key.
- `delay` — Delay between requests, in seconds.

## Catalogue notes

Get access to accurate Whois records for generic and country TLDs. Around 1000 gTLDs include .com, .org, .net, .us, .biz, .info, .mobi, .pro, .asia and many other new ones.
Raw and parsed Whois data are both accessible for downloads in the form of MYSQL or MYSQL database dumps and Comma Separated Values (.CSV) files.
