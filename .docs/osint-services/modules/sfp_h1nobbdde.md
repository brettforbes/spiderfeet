# HackerOne (Unofficial)

**Module ID:** `sfp_h1nobbdde`

## Summary

Check external vulnerability scanning/reporting service h1.nobbd.de to see if the target is listed.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://www.nobbd.de/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** http://www.nobbd.de/index.php#projekte, https://twitter.com/disclosedh1

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `VULNERABILITY_DISCLOSURE`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DOMAIN_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss
