# Account Finder

**Module ID:** `sfp_accounts`

## Summary

Look for possible associated accounts on over 500 social and other websites such as Instagram, Reddit, etc.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_accounts
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_accounts

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- `DOMAIN_NAME`
- `HUMAN_NAME`
- `USERNAME`
- **Produced:**
- `USERNAME`
- `ACCOUNT_EXTERNAL_OWNED`
- `SIMILAR_ACCOUNT_EXTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Passive

## Module options

- `_maxthreads` — Maximum threads
- `ignorenamedict` — Don't bother looking up names that are just stand-alone first names (too many false positives).
- `ignoreworddict` — Don't bother looking up names that appear in the dictionary.
- `musthavename` — The username must be mentioned on the social media page to consider it valid (helps avoid false positives).
- `permutate` — Look for the existence of account name permutations. Useful to identify fraudulent social media accounts or account squatting.
- `userfromemail` — Extract usernames from e-mail addresses at all? If disabled this can reduce false positives for common usernames but for highly unique usernames it would result in missed accounts.
- `usernamesize` — The minimum length of a username to query across social media sites. Helps avoid false positives for very common short usernames.

## Test seeds

- `EMAILADDR`: input=`noreply@spiderfoot.net` validation=smoke status=UNKNOWN; verdict=clean_miss; produced=0

## Catalogue notes

Look for possible associated accounts on over 500 social and other websites such as Instagram, Reddit, etc.

**Module ID:** `sfp_accounts`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** EMAILADDR, DOMAIN_NAME, HUMAN_NAME, USERNAME
**Produces:** USERNAME, ACCOUNT_EXTERNAL_OWNED, SIMILAR_ACCOUNT_EXTERNAL

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `EMAILADDR`
- Input: `noreply@spiderfoot.net`
- Produced count: 0
