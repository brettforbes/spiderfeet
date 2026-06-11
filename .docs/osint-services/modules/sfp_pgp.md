# PGP Key Servers

**Module ID:** `sfp_pgp`

## Summary

Look up domains and e-mail addresses in PGP public key servers.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_pgp
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_pgp

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `INTERNET_NAME`
- `EMAILADDR`
- `DOMAIN_NAME`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `AFFILIATE_EMAILADDR`
- `PGP_KEY`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `keyserver_fetch1` — PGP public key server URL to find the public key for an e-mail address. Email address will get appended.
- `keyserver_fetch2` — Backup PGP public key server URL to find the public key for an e-mail address. Email address will get appended.
- `keyserver_search1` — PGP public key server URL to find e-mail addresses on a domain. Domain will get appended.
- `keyserver_search2` — Backup PGP public key server URL to find e-mail addresses on a domain. Domain will get appended.
- `retrieve_keys` — Retrieve PGP keys.

## Test seeds

- `EMAILADDR`: input=`security@gnu.org` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Look up domains and e-mail addresses in PGP public key servers.

**Module ID:** `sfp_pgp`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, EMAILADDR, DOMAIN_NAME
**Produces:** EMAILADDR, EMAILADDR_GENERIC, AFFILIATE_EMAILADDR, PGP_KEY

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `EMAILADDR`
- Input: `security@gnu.org`
- Produced count: 1
