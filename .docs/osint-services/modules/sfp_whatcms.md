# WhatCMS

**Module ID:** `sfp_whatcms`

## Summary

Check web technology using WhatCMS.org API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://whatcms.org/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://whatcms.org/API, https://whatcms.org/Documentation

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** apikey, slow
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — WhatCMS API key
- `delay` — Delay between requests, in seconds.
- `timeout` — Query timeout, in seconds.
