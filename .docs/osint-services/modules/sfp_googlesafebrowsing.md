# Google SafeBrowsing

**Module ID:** `sfp_googlesafebrowsing`

## Summary

Check if the URL is included on any of the Safe Browsing lists.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://developers.google.com/safe-browsing/v4/lookup-api
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://developers.google.com/safe-browsing/v4/reference/rest

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
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** slow, apikey
- **Categories:** Reputation Systems
- **Use cases:** Passive, Investigate

## Module options

- `api_key` — Google Safe Browsing API key.

## Catalogue notes

The Safe Browsing APIs (v4) let your client applications check URLs against Google's constantly updated lists of unsafe web resources. Any URL found on a Safe Browsing list is considered unsafe.
