# F-Secure Riddler.io

**Module ID:** `sfp_fsecure_riddler`

## Summary

Obtain network information from F-Secure Riddler.io API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://riddler.io/
- **Model:** `PRIVATE_ONLY`
- **References:** https://riddler.io/help/api, https://riddler.io/help/search, https://riddler.io/static/riddler_white_paper.pdf, https://www.f-secure.com/en/business/products/vulnerability-management/radar

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `IP_ADDRESS`
- **Produced:**
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `INTERNET_NAME_UNRESOLVED`
- `AFFILIATE_INTERNET_NAME_UNRESOLVED`
- `DOMAIN_NAME`
- `AFFILIATE_DOMAIN_NAME`
- `IP_ADDRESS`
- `PHYSICAL_COORDINATES`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Footprint, Passive

## Module options

- `password` — F-Secure Riddler.io password
- `username` — F-Secure Riddler.io username
- `verify` — Verify host names resolve

## Catalogue notes

Riddler.io allows you to search in a high quality dataset with more than 396,831,739 hostnames. Unlike others, we do not rely on simple port scanning techniques - we crawl the web, ensuring an in-depth quality data set you will not find anywhere else.
Use Riddler to enumerate possible attack vectors during your pen-test or use the very same data to monitor potential threats before it is too late.
