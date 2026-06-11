# Bitcoin Who's Who

**Module ID:** `sfp_bitcoinwhoswho`

## Summary

Check for Bitcoin addresses against the Bitcoin Who's Who database of suspect/malicious addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://bitcoinwhoswho.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://bitcoinwhoswho.com/api

## Routes

- **Route seed nugget:** `BITCOIN_ADDRESS`
- **Consumed:**
- `BITCOIN_ADDRESS`
- **Produced:**
- `MALICIOUS_BITCOIN_ADDRESS`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Passive, Investigate

## Module options

- `api_key` — Bitcoin Who's Who API Key.

## Catalogue notes

Bitcoin Who's Who is dedicated to profiling the extraordinary members of the bitcoin ecosystem.Our goal is to help you verify a bitcoin address owner and avoid a bitcoin scam or fraud.
