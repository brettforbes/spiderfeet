# ProjectDiscovery Chaos

**Module ID:** `sfp_projectdiscovery`

## Summary

Search for hosts/subdomains using chaos.projectdiscovery.io

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://chaos.projectdiscovery.io
- **Model:** `PRIVATE_ONLY`
- **References:** https://chaos.projectdiscovery.io/#/docs, https://projectdiscovery.io/privacy, https://projectdiscovery.io/about

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `api_key` — chaos.projectdiscovery.io API Key.
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Catalogue notes

Projectdiscovery Chaos actively collect and maintain internet-wide assets' data, this project is meant to enhance research and analyse changes around DNS for better insights.
