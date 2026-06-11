# URLScan.io

**Module ID:** `sfp_urlscan`

## Summary

Search URLScan.io cache for domain information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://urlscan.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://urlscan.io/about-api/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `GEOINFO`
- `LINKED_URL_INTERNAL`
- `RAW_RIR_DATA`
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `BGP_AS_MEMBER`
- `WEBSERVER_BANNER`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `verify` — Verify that any hostnames found on the target domain still resolve?

## Test seeds

- `INTERNET_NAME`: input=`bbc.co.uk` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

urlscan.io is a service to scan and analyse websites. When a URL is submitted to urlscan.io, an automated process will browse to the URL like a regular user and record the activity that this page navigation creates. This includes the domains and IPs contacted, the resources (JavaScript, CSS, etc) requested from those domains, as well as additional information about the page itself. urlscan.io will take a screenshot of the page, record the DOM content, JavaScript global variables, cookies created by the page, and a myriad of other observations.
