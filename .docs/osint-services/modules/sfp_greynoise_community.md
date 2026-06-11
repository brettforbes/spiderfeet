# GreyNoise Community

**Module ID:** `sfp_greynoise_community`

## Summary

Obtain IP enrichment data from GreyNoise Community API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://greynoise.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.greynoise.io/reference/get_v3-community-ip, https://viz.greynoise.io/signup

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- **Produced:**
- `MALICIOUS_IPADDR`
- `COMPANY_NAME`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `age_limit_days` — Ignore any records older than this many days. 0 = unlimited.
- `api_key` — GreyNoise Community API Key.

## Catalogue notes

At GreyNoise, we collect and analyze untargeted, widespread, and opportunistic scan and attack activity that reaches every server directly connected to the Internet. Mass scanners (such as Shodan and Censys), search engines, bots, worms, and crawlers generate logs and events omnidirectionally on every IP address in the IPv4 space. GreyNoise gives you the ability to filter this useless noise out.
