# Snov

**Module ID:** `sfp_snov`

## Summary

Gather available email IDs from identified domains

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://snov.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://snov.io/api

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key_client_id` — Snov.io API Client ID
- `api_key_client_secret` — Snov.io API Client Secret

## Catalogue notes

Snov.io API allows to get a list of all emails from a particular domain, find email addresses by name and domain, verify emails, add prospects to a list, change a recipient's status and more.
