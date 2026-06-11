# NeutrinoAPI

**Module ID:** `sfp_neutrinoapi`

## Summary

Search NeutrinoAPI for phone location information, IP address information, and host reputation.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.neutrinoapi.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://www.neutrinoapi.com/api/api-basics/, https://www.neutrinoapi.com/api/phone-validate/, https://www.neutrinoapi.com/api/ip-info/, https://www.neutrinoapi.com/api/ip-blocklist/, https://www.neutrinoapi.com/api/host-reputation/

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `PHONE_NUMBER`
- **Produced:**
- `RAW_RIR_DATA`
- `BLACKLISTED_IPADDR`
- `MALICIOUS_IPADDR`
- `PROXY_HOST`
- `VPN_HOST`
- `TOR_EXIT_NODE`
- `GEOINFO`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — NeutrinoAPI API key.
- `timeout` — Query timeout, in seconds.
- `user_id` — NeutrinoAPI user ID.
