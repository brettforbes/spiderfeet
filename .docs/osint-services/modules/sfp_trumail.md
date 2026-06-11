# Trumail

**Module ID:** `sfp_trumail`

## Summary

Check whether an email is disposable

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://trumail.io/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://trumail.io/documentation

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `EMAILADDR_DISPOSABLE`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `EMAILADDR`: input=`noreply@spiderfoot.net` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Trumail is a product that was built with the intention of providing an easy to use API to software professionals who value a quality audience. Your apps registration workflow is one of the most important and complex parts of your software and it's very important that you filter user credentials in a way that allows for future use. Invalid user credentials, particularly email addresses, should be deemed valid and deliverable at the time of signup - That's where we come in.
