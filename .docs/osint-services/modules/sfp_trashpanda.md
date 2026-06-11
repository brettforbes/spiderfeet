# Trashpanda

**Module ID:** `sfp_trashpanda`

## Summary

Queries Trashpanda to gather intelligence about mentions of target in pastesites

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://got-hacked.wtf
- **Model:** `FREE_AUTH_LIMITED`
- **References:** http://api.got-hacked.wtf:5580/help

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `INTERNET_NAME`
- `EMAILADDR`
- **Produced:**
- `LEAKSITE_CONTENT`
- `LEAKSITE_URL`
- `PASSWORD_COMPROMISED`

## Flags and categories

- **Flags:** apikey
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Investigate, Passive

## Module options

- `api_key_password` — Trashpanda API Password
- `api_key_username` — Trashpanda API Username

## Catalogue notes

The bot searches different paste sites for leaked credentials.The API itself gives access to all unique credentials the bot ever detected.
