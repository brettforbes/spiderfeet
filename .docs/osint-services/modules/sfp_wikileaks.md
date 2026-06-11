# Wikileaks

**Module ID:** `sfp_wikileaks`

## Summary

Search Wikileaks for mentions of domain names and e-mail addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://wikileaks.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://wikileaks.org/-Leaks-.html#submit, https://wikileaks.org/What-is-WikiLeaks.html

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `EMAILADDR`
- `HUMAN_NAME`
- **Produced:**
- `LEAKSITE_CONTENT`
- `LEAKSITE_URL`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `daysback` — How many days back to consider a leak valid for capturing. 0 = unlimited.
- `external` — Include external leak sources such as Associated Twitter accounts, Snowden + Hammond Documents, Cryptome Documents, ICWatch, This Day in WikiLeaks Blog and WikiLeaks Press, WL Central.

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

WikiLeaks specializes in the analysis and publication of large datasets of censored or otherwise restricted official materials involving war, spying and corruption. It has so far published more than 10 million documents and associated analyses.
