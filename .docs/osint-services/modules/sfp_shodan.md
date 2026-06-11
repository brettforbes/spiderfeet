# SHODAN

**Module ID:** `sfp_shodan`

## Summary

Obtain information from SHODAN about identified IP addresses.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.shodan.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://developer.shodan.io/api, https://developer.shodan.io/apps

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- `DOMAIN_NAME`
- `WEB_ANALYTICS_ID`
- **Produced:**
- `OPERATING_SYSTEM`
- `DEVICE_TYPE`
- `TCP_PORT_OPEN`
- `TCP_PORT_OPEN_BANNER`
- `RAW_RIR_DATA`
- `GEOINFO`
- `IP_ADDRESS`
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`
- `VULNERABILITY_GENERAL`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `api_key` — SHODAN API Key.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible hosts on the same target subdomain/domain?

## Catalogue notes

Shodan is the world's first search engine for Internet-connected devices.
Use Shodan to discover which of your devices are connected to the Internet, where they are located and who is using them.Keep track of all the computers on your network that are directly accessible from the Internet. Shodan lets you understand your digital footprint.
