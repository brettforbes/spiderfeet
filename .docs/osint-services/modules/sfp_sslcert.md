# SSL Certificate Analyzer

**Module ID:** `sfp_sslcert`

## Summary

Gather information about SSL certificates used by the target's HTTPS sites.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_sslcert
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_sslcert

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `LINKED_URL_INTERNAL`
- `IP_ADDRESS`
- **Produced:**
- `TCP_PORT_OPEN`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `CO_HOSTED_SITE`
- `CO_HOSTED_SITE_DOMAIN`
- `SSL_CERTIFICATE_ISSUED`
- `SSL_CERTIFICATE_ISSUER`
- `SSL_CERTIFICATE_MISMATCH`
- `SSL_CERTIFICATE_EXPIRED`
- `SSL_CERTIFICATE_EXPIRING`
- `SSL_CERTIFICATE_RAW`
- `DOMAIN_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `certexpiringdays` — Number of days in the future a certificate expires to consider it as expiring.
- `ssltimeout` — Seconds before giving up trying to HTTPS connect.
- `tryhttp` — Also try to HTTPS-connect to HTTP sites and hostnames.
- `verify` — Verify certificate subject alternative names resolve.

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=UNKNOWN; verdict=hit; produced=4

## Catalogue notes

Gather information about SSL certificates used by the target's HTTPS sites.

**Module ID:** `sfp_sslcert`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, LINKED_URL_INTERNAL, IP_ADDRESS
**Produces:** TCP_PORT_OPEN, INTERNET_NAME, INTERNET_NAME_UNRESOLVED, CO_HOSTED_SITE, CO_HOSTED_SITE_DOMAIN, SSL_CERTIFICATE_ISSUED, SSL_CERTIFICATE_ISSUER, SSL_CERTIFICATE_MISMATCH…

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
