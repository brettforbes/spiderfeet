# Template Module

**Module ID:** `sfp_template`

## Summary

This is an example module to help developers create their own SpiderFeet modules.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.datasource.com
- **Model:** `FREE_NOAUTH_LIMITED`
- **References:** https://www.datasource.com/api-documentation

## CLI / tool

- **Tool:** Nmap
- **Website:** https://tool.org
- **Repository:** https://github.com/author/tool

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
- `VULNERABILITY_GENERAL`

## Flags and categories

- **Flags:** slow, apikey
- **Categories:** Social Media
- **Use cases:** Passive

## Module options

- `api_key` — SomeDataource API Key.
- `checkaffiliates` — Check affiliates?
- `checkcohosts` — Check co-hosted sites?
- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Catalogue notes

A paragraph of text with details about the data source / services. Keep things neat by breaking the text up across multiple lines as has been done here. If line breaks are needed for breaking up multiple paragraphs, use 
.
