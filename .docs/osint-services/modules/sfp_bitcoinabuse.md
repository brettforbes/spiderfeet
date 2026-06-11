# BitcoinAbuse

**Module ID:** `sfp_bitcoinabuse`

## Summary

Check Bitcoin addresses against the bitcoinabuse.com database of suspect/malicious addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.bitcoinabuse.com/
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://www.bitcoinabuse.com/api-docs

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

- `api_key` — BitcoinAbuse API Key.

## Catalogue notes

BitcoinAbuse.com is a public database of bitcoin addresses used by scammers, hackers, and criminals.Bitcoin is anonymous if used perfectly. Luckily, no one is perfect. Even hackers make mistakes. It only takes one slip to link stolen bitcoin to a hacker's their real identity. It is our hope that by making a public database of bitcoin addresses used by criminals it will be harder for criminals to convert the digital currency back into fiat money.
