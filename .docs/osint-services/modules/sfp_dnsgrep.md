# DNSGrep

**Module ID:** `sfp_dnsgrep`

## Summary

Obtain Passive DNS information from Rapid7 Sonar Project using DNSGrep API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://opendata.rapid7.com/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://opendata.rapid7.com/apihelp/, https://www.rapid7.com/about/research

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `dns_resolve` — DNS resolve each identified domain.
- `timeout` — Query timeout, in seconds.

## Catalogue notes

Offering researchers and community members open access to data from Project Sonar, which conducts internet-wide surveys to gain insights into global exposure to common vulnerabilities.
