# Host.io

**Module ID:** `sfp_hostio`

## Summary

Obtain information about domain names from host.io.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://host.io
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://host.io/docs

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `IP_ADDRESS`
- `RAW_RIR_DATA`
- `EMAILADDR`
- `WEB_ANALYTICS_ID`
- `WEBSERVER_TECHNOLOGY`
- `PHYSICAL_COORDINATES`
- `DESCRIPTION_ABSTRACT`
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Passive DNS
- **Use cases:** Passive

## Module options

- `api_key` — Host.io API Key.

## Catalogue notes

We collect data on every known domain name, from every TLD, and update it every month. Our data includes DNS records and website data for each of the domains.We process terabytes of data and summarize it to produce our final results. Browse through our site to see backlinks, redirects, server details or IP address and hosting provider details courtesy of IPinfo.io.
