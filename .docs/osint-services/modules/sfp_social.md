# Social Network Identifier

**Module ID:** `sfp_social`

## Summary

Identify presence on social media networks such as LinkedIn, Twitter and others.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_social
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_social

## Routes

- **Route seed nugget:** `LINKED_URL_EXTERNAL`
- **Consumed:**
- `LINKED_URL_EXTERNAL`
- **Produced:**
- `SOCIAL_MEDIA`
- `USERNAME`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Passive

## Test seeds

- `LINKED_URL_EXTERNAL`: input=`https://twitter.com/example` validation=smoke status=UNKNOWN; verdict=hit; produced=2

## Catalogue notes

Identify presence on social media networks such as LinkedIn, Twitter and others.

**Module ID:** `sfp_social`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_EXTERNAL
**Produces:** SOCIAL_MEDIA, USERNAME

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
