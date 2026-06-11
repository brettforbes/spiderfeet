# Whoisology

**Module ID:** `sfp_whoisology`

## Summary

Reverse Whois lookups using Whoisology.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `paid_auth (paid)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://whoisology.com/
- **Model:** `COMMERCIAL_ONLY`
- **References:** https://whoisology.com/whois-database-download, https://whoisology.com/tutorial

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_DOMAIN_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Investigate, Passive

## Module options

- `api_key` — Whoisology.com API key.

## Catalogue notes

Whoisology is a domain name ownership archive with literally billions of searchable and cross referenced domain name whois records.
Our main focus is reverse whois which is used for cyber crime investigation / InfoSec, corporate intelligence, legal research, business development, and for good ol' fashioned poking around.
