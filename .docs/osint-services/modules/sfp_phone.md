# Phone Number Extractor

**Module ID:** `sfp_phone`

## Summary

Identify phone numbers in scraped webpages.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_phone
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_phone

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `PHONE_NUMBER`
- **Produced:**
- `PHONE_NUMBER`
- `PROVIDER_TELCO`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Passive, Footprint, Investigate

## Test seeds

- `TARGET_WEB_CONTENT`: input=`Call us on +1-212-555-1212` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify phone numbers in scraped webpages.

**Module ID:** `sfp_phone`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, DOMAIN_WHOIS, NETBLOCK_WHOIS, PHONE_NUMBER
**Produces:** PHONE_NUMBER, PROVIDER_TELCO

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `Call us on +1-555-0100`
- Produced count: 0
