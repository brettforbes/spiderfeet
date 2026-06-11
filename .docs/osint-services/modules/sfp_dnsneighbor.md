# DNS Look-aside

**Module ID:** `sfp_dnsneighbor`

## Summary

Attempt to reverse-resolve the IP addresses next to your target to see if they are related.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_dnsneighbor
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_dnsneighbor

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- **Produced:**
- `AFFILIATE_IPADDR`
- `IP_ADDRESS`

## Flags and categories

- **Flags:** —
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Module options

- `lookasidebits` — If look-aside is enabled, the netmask size (in CIDR notation) to check. Default is 4 bits (16 hosts).
- `validatereverse` — Validate that reverse-resolved hostnames still resolve back to that IP before considering them as aliases of your target.

## Test seeds

- `IP_ADDRESS`: input=`1.1.1.1` validation=smoke status=UNKNOWN; verdict=hit; produced=2

## Catalogue notes

Attempt to reverse-resolve the IP addresses next to your target to see if they are related.

**Module ID:** `sfp_dnsneighbor`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS
**Produces:** AFFILIATE_IPADDR, IP_ADDRESS

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `NETBLOCK_MEMBER`
- Input: `8.8.8.0/24`
- Produced count: 0
