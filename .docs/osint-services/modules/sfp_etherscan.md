# Etherscan

**Module ID:** `sfp_etherscan`

## Summary

Queries etherscan.io to find the balance of identified ethereum wallet addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://etherscan.io
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://etherscan.io/apis

## Routes

- **Route seed nugget:** `ETHEREUM_ADDRESS`
- **Consumed:**
- `ETHEREUM_ADDRESS`
- **Produced:**
- `ETHEREUM_BALANCE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — API Key for etherscan.io
- `pause` — Number of seconds to wait between each API call.

## Catalogue notes

Etherscan allows you to explore and search the Ethereum blockchain for transactions, addresses, tokens, prices and other activities taking place on Ethereum (ETH)
