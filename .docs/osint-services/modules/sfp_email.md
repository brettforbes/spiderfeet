# E-Mail Address Extractor

**Module ID:** `sfp_email`

## Summary

Identify e-mail addresses in any obtained data.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_email
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_email

## Routes

- **Route seed nugget:** `AFFILIATE_DOMAIN_WHOIS`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `BASE64_DATA`
- `AFFILIATE_DOMAIN_WHOIS`
- `CO_HOSTED_SITE_DOMAIN_WHOIS`
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `LEAKSITE_CONTENT`
- `RAW_DNS_RECORDS`
- `RAW_FILE_META_DATA`
- `RAW_RIR_DATA`
- `SIMILARDOMAIN_WHOIS`
- `SSL_CERTIFICATE_RAW`
- `SSL_CERTIFICATE_ISSUED`
- `TCP_PORT_OPEN_BANNER`
- `WEBSERVER_BANNER`
- `WEBSERVER_HTTPHEADERS`
- **Produced:**
- `EMAILADDR`
- `EMAILADDR_GENERIC`
- `AFFILIATE_EMAILADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Passive, Investigate, Footprint

## Test seeds

- `AFFILIATE_DOMAIN_WHOIS`: input=`Admin Email: admin@example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify e-mail addresses in any obtained data.

**Module ID:** `sfp_email`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, BASE64_DATA, AFFILIATE_DOMAIN_WHOIS, CO_HOSTED_SITE_DOMAIN_WHOIS, DOMAIN_WHOIS, NETBLOCK_WHOIS, LEAKSITE_CONTENT, RAW_DNS_RECORDS…
**Produces:** EMAILADDR, EMAILADDR_GENERIC, AFFILIATE_EMAILADDR

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `AFFILIATE_DOMAIN_WHOIS`
- Input: `Admin Email: admin@example.com`
- Produced count: 1
