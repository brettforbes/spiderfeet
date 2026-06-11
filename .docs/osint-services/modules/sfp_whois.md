# Whois

**Module ID:** `sfp_whois`

## Summary

Perform a WHOIS look-up on domain names and owned netblocks.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_whois
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_whois

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- `DOMAIN_NAME_PARENT`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- `CO_HOSTED_SITE_DOMAIN`
- `AFFILIATE_DOMAIN_NAME`
- `SIMILARDOMAIN`
- **Produced:**
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `DOMAIN_REGISTRAR`
- `CO_HOSTED_SITE_DOMAIN_WHOIS`
- `AFFILIATE_DOMAIN_WHOIS`
- `SIMILARDOMAIN_WHOIS`

## Flags and categories

- **Flags:** —
- **Categories:** Public Registries
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=2

## Catalogue notes

Perform a WHOIS look-up on domain names and owned netblocks.

**Module ID:** `sfp_whois`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** DOMAIN_NAME, DOMAIN_NAME_PARENT, NETBLOCK_OWNER, NETBLOCKV6_OWNER, CO_HOSTED_SITE_DOMAIN, AFFILIATE_DOMAIN_NAME, SIMILARDOMAIN
**Produces:** DOMAIN_WHOIS, NETBLOCK_WHOIS, DOMAIN_REGISTRAR, CO_HOSTED_SITE_DOMAIN_WHOIS, AFFILIATE_DOMAIN_WHOIS, SIMILARDOMAIN_WHOIS

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 2
