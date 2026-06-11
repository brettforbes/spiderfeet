# Clearbit

**Module ID:** `sfp_clearbit`

## Summary

Check for names, addresses, domains and more based on lookups of e-mail addresses on clearbit.com.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://clearbit.com/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://clearbit.com/docs

## Routes

- **Route seed nugget:** `EMAILADDR`
- **Consumed:**
- `EMAILADDR`
- **Produced:**
- `RAW_RIR_DATA`
- `PHONE_NUMBER`
- `PHYSICAL_ADDRESS`
- `AFFILIATE_INTERNET_NAME`
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `INTERNET_NAME`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — Clearbit.com API key.

## Catalogue notes

Clearbit is the marketing data engine for all of your customer interactions. Deeply understand your customers, identify future prospects, and personalize every single marketing and sales interaction.
Rely on fresh, accurate data with our proprietary real-time lookups. Then act on new information immediately, with sales alerting and job change notifications.
Get company attributes like employee count, technologies used, and industry classification—and get employee details like role, seniority, and even job change notifications, right at your fingertips.
With our dataset and machine learning algorithms, you’ll have all of the information you need to convert leads and grow your business.
