# Twilio

**Module ID:** `sfp_twilio`

## Summary

Obtain information from Twilio about phone numbers. Ensure you have the Caller Name add-on installed in Twilio.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.twilio.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://www.twilio.com/docs/all, https://www.twilio.com/blog/what-does-twilio-do

## Routes

- **Route seed nugget:** `PHONE_NUMBER`
- **Consumed:**
- `PHONE_NUMBER`
- **Produced:**
- `COMPANY_NAME`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key_account_sid` — Twilio Account SID
- `api_key_auth_token` — Twilio Auth Token

## Catalogue notes

Twilio is a cloud communications platform as a service company based in San Francisco, California. Twilio allows software developers to programmatically make and receive phone calls, send and receive text messages, and perform other communication functions using its web service APIs.
