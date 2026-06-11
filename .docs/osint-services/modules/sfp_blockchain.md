# Blockchain

**Module ID:** `sfp_blockchain`

## Summary

Queries blockchain.info to find the balance of identified bitcoin wallet addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://www.blockchain.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://exchange.blockchain.com/api/#introduction, https://exchange.blockchain.com/markets, https://exchange.blockchain.com/fees, https://exchange.blockchain.com/trade

## Routes

- **Route seed nugget:** `BITCOIN_ADDRESS`
- **Consumed:**
- `BITCOIN_ADDRESS`
- **Produced:**
- `BITCOIN_BALANCE`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `BITCOIN_ADDRESS`: input=`1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` validation=smoke status=FINISHED; verdict=hit

## Catalogue notes

Blockchain Exchange is the most secure place to buy, sell, and trade crypto.
Use the most popular block explorer to search and verify transactions on the Bitcoin, Ethereum, and Bitcoin Cash blockchains.
Stay on top of Bitcoin and other top cryptocurrency prices, news, and market information.
