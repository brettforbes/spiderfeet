# Country Name Extractor

**Module ID:** `sfp_countryname`

## Summary

Identify country names in any obtained data.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_countryname
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_countryname

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `IBAN_NUMBER`
- `PHONE_NUMBER`
- `AFFILIATE_DOMAIN_NAME`
- `CO_HOSTED_SITE_DOMAIN`
- `DOMAIN_NAME`
- `SIMILARDOMAIN`
- `AFFILIATE_DOMAIN_WHOIS`
- `CO_HOSTED_SITE_DOMAIN_WHOIS`
- `DOMAIN_WHOIS`
- `GEOINFO`
- `PHYSICAL_ADDRESS`
- **Produced:**
- `COUNTRY_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `affiliate` — Obtain country name from affiliate sites
- `cohosted` — Obtain country name from co-hosted sites
- `noncountrytld` — Parse TLDs not associated with any country as default country domains
- `similardomain` — Obtain country name from similar domains

## Test seeds

- `TARGET_WEB_CONTENT`: input=`Server located in United States` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify country names in any obtained data.

**Module ID:** `sfp_countryname`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IBAN_NUMBER, PHONE_NUMBER, AFFILIATE_DOMAIN_NAME, CO_HOSTED_SITE_DOMAIN, DOMAIN_NAME, SIMILARDOMAIN, AFFILIATE_DOMAIN_WHOIS, CO_HOSTED_SITE_DOMAIN_WHOIS…
**Produces:** COUNTRY_NAME

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `Server located in United States`
- Produced count: 1
