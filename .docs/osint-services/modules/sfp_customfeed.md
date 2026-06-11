# Custom Threat Feed

**Module ID:** `sfp_customfeed`

## Summary

Check if a host/domain, netblock, ASN or IP is malicious according to your custom feed.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_customfeed
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_customfeed

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `CO_HOSTED_SITE`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_COHOST`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Maximum age of data in hours before re-downloading. 0 to always download.
- `checkaffiliates` — Apply checks to affiliates?
- `checkcohosts` — Apply checks to sites found to be co-hosted on the target's IP?
- `url` — The URL where the feed can be found. Exact matching is performed so the format must be a single line per host, ASN, domain, IP or netblock.

## Test seeds

- `INTERNET_NAME`: input=`evil-smoke.example.com` validation=smoke smoke

## Catalogue notes

Check if a host/domain, netblock, ASN or IP is malicious according to your custom feed.

**Module ID:** `sfp_customfeed`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, IP_ADDRESS, AFFILIATE_INTERNET_NAME, AFFILIATE_IPADDR, CO_HOSTED_SITE
**Produces:** MALICIOUS_IPADDR, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_IPADDR, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `INTERNET_NAME`
- Input: `8.8.8.8`
- Produced count: 0
