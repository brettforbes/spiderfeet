# Venmo

**Module ID:** `sfp_venmo`

## Summary

Gather user information from Venmo API.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** https://venmo.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`

## Routes

- **Route seed nugget:** `USERNAME`
- **Consumed:**
- `USERNAME`
- **Produced:**
- `RAW_RIR_DATA`
- `HUMAN_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Social Media
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `USERNAME`: input=`paypal` validation=smoke status=FINISHED; verdict=hit; Pass 3 targeted probe; status=FINISHED

## Catalogue notes

Venmo is a digital wallet that allows you to send money and make purchases at approved merchants.
