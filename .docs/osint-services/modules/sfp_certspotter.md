# CertSpotter

**Module ID:** `sfp_certspotter`

## Summary

Gather information about SSL certificates from SSLMate CertSpotter API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://sslmate.com/certspotter/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://sslmate.com/help/reference/ct_search_api_v1

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`
- `CO_HOSTED_SITE`
- `CO_HOSTED_SITE_DOMAIN`
- `SSL_CERTIFICATE_ISSUED`
- `SSL_CERTIFICATE_ISSUER`
- `SSL_CERTIFICATE_MISMATCH`
- `SSL_CERTIFICATE_EXPIRED`
- `SSL_CERTIFICATE_EXPIRING`
- `SSL_CERTIFICATE_RAW`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — CertSpotter API key.
- `certexpiringdays` — Number of days in the future a certificate expires to consider it as expiring.
- `max_pages` — Maximum number of pages of results to fetch.
- `verify` — Verify certificate subject alternative names resolve.

## Catalogue notes

Cert Spotter monitors your domains for expiring, unauthorized, and invalid SSL certificates, so you can act before an incident, not after.
