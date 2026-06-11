# Company Name Extractor

**Module ID:** `sfp_company`

## Summary

Identify company names in any obtained data.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_company
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_company

## Routes

- **Route seed nugget:** `AFFILIATE_DOMAIN_WHOIS`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `SSL_CERTIFICATE_ISSUED`
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `AFFILIATE_DOMAIN_WHOIS`
- `AFFILIATE_WEB_CONTENT`
- **Produced:**
- `COMPANY_NAME`
- `AFFILIATE_COMPANY_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `filterjscss` — Filter out company names that originated from CSS/JS content. Enabling this avoids detection of popular Javascript and web framework author company names.

## Test seeds

- `AFFILIATE_DOMAIN_WHOIS`: input=`Registrant Organization: Example Corp
Registrant Country: US` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify company names in any obtained data.

**Module ID:** `sfp_company`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, SSL_CERTIFICATE_ISSUED, DOMAIN_WHOIS, NETBLOCK_WHOIS, AFFILIATE_DOMAIN_WHOIS, AFFILIATE_WEB_CONTENT
**Produces:** COMPANY_NAME, AFFILIATE_COMPANY_NAME

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `AFFILIATE_DOMAIN_WHOIS`
- Input: `Registrant Organization: Example Corp
Registrant Country: US`
- Produced count: 1
