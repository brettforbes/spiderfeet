# CIRCL.LU

**Module ID:** `sfp_circllu`

## Summary

Obtain information from CIRCL.LU's Passive DNS and Passive SSL databases.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.circl.lu/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://www.circl.lu/services/passive-dns/, https://www.circl.lu/services/passive-ssl/, https://www.circl.lu/services/, https://www.circl.lu/pub/, https://www.circl.lu/projects

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `NETBLOCK_OWNER`
- `IP_ADDRESS`
- `DOMAIN_NAME`
- **Produced:**
- `IP_ADDRESS`
- `SSL_CERTIFICATE_ISSUED`
- `CO_HOSTED_SITE`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any Passive DNS records older than this many days. 0 = unlimited.
- `api_key_login` — CIRCL.LU login.
- `api_key_password` — CIRCL.LU password.
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `verify` — Verify co-hosts are valid by checking if they still resolve to the shared IP.

## Catalogue notes

The Computer Incident Response Center Luxembourg (CIRCL) is a government-driven initiative designed to gather, review, report and respond to computer security threats and incidents.
CIRCL provides a reliable and trusted point of contact for any users, companies and organizations based in Luxembourg, for the handling of attacks and incidents. Its team of experts acts like a fire brigade, with the ability to react promptly and efficiently whenever threats are suspected, detected or incidents occur.
