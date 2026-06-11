# Certificate Transparency

**Module ID:** `sfp_crt`

## Summary

Gather hostnames from historical certificates in crt.sh.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://crt.sh/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://sectigo.com/, https://github.com/crtsh

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `SSL_CERTIFICATE_RAW`
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`
- `CO_HOSTED_SITE`
- `CO_HOSTED_SITE_DOMAIN`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `fetchcerts` — Fetch each certificate found, for processing by other modules.
- `verify` — Verify certificate subject alternative names resolve.

## Test seeds

- `DOMAIN_NAME`: input=`google.com` validation=blocked-upstream SPEC_GAP upstream: crt.sh returns errors/unavailable JSON for automated queries (rate-limit or outage)
- `INTERNET_NAME`: input=`google.com` validation=pilot pilot
