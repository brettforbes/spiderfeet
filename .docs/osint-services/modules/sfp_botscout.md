# BotScout

**Module ID:** `sfp_botscout`

## Summary

Searches BotScout.com's database of spam-bot IP addresses and e-mail addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://botscout.com/
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** http://botscout.com/api.htm, http://botscout.com/api_queries.htm, http://botscout.com/getkey.htm, http://botscout.com/corp_users.htm

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `EMAILADDR`
- **Produced:**
- `MALICIOUS_IPADDR`
- `BLACKLISTED_IPADDR`
- `MALICIOUS_EMAILADDR`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Passive, Investigate

## Module options

- `api_key` — Botscout.com API key. Without this you will be limited to 100 look-ups per day.

## Catalogue notes

BotScout helps prevent automated web scripts, known as "bots", from registering on forums, polluting databases, spreading spam, and abusing forms on web sites. We do this by tracking the names, IPs, and email addresses that bots use and logging them as unique signatures for future reference. We also provide a simple yet powerful API that you can use to test forms when they're submitted on your site.
