# EmailRep

**Module ID:** `sfp_emailrep`

## Summary

Search EmailRep.io for email address reputation.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://emailrep.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.emailrep.io/

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `RAW_RIR_DATA`
- `EMAILADDR_COMPROMISED`
- `MALICIOUS_EMAILADDR`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — EmailRep API key.

## Catalogue notes

Illuminate the "reputation" behind an email address.
EmailRep uses hundreds of factors like domain age, traffic rankings, presence on social media sites, professional networking sites, personal connections, public records, deliverability, data breaches, dark web credential leaks, phishing emails, threat actor emails, and more to answer these types of questions.
