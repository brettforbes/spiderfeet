# TextMagic

**Module ID:** `sfp_textmagic`

## Summary

Obtain phone number type from TextMagic API

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.textmagic.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.textmagic.com/

## Routes

- **Route seed nugget:** `PHONE_NUMBER`
- **Consumed:**
- `PHONE_NUMBER`
- **Produced:**
- `PHONE_NUMBER_TYPE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Passive

## Module options

- `api_key` — TextMagic API Key
- `api_key_username` — TextMagic API Username

## Catalogue notes

TextMagic is a business text-messaging service for sending notifications, alerts, reminders, confirmations and SMS marketing campaigns.
