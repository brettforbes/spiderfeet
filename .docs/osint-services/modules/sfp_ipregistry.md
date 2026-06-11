# ipregistry

**Module ID:** `sfp_ipregistry`

## Summary

Query the ipregistry.co database for reputation and geo-location.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://ipregistry.co/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://ipregistry.co/docs

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- **Produced:**
- `GEOINFO`
- `MALICIOUS_IPADDR`
- `PHYSICAL_COORDINATES`
- `RAW_RIR_DATA`

## Flags and categories

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Passive, Footprint, Investigate

## Module options

- `api_key` — Ipregistry API Key.

## Catalogue notes

Ipregistry is a trusted and in-depth IP Geolocation and Threat detections source of information that canbenefit publishers, ad networks, retailers, financial services, e-commerce stores and more.
