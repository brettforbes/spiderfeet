# BinaryEdge

**Module ID:** `sfp_binaryedge`

## Summary

Obtain information from BinaryEdge.io Internet scanning systems, including breaches, vulnerabilities, torrents and passive DNS.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.binaryedge.io/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.binaryedge.io/, https://www.binaryedge.io/data.html

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `DOMAIN_NAME`
- `EMAILADDR`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `INTERNET_NAME`
- `DOMAIN_NAME`
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`
- `VULNERABILITY_GENERAL`
- `TCP_PORT_OPEN`
- `TCP_PORT_OPEN_BANNER`
- `EMAILADDR_COMPROMISED`
- `UDP_PORT_OPEN`
- `UDP_PORT_OPEN_INFO`
- `CO_HOSTED_SITE`
- `MALICIOUS_IPADDR`

## Flags and categories

- **Flags:** apikey
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `binaryedge_api_key` — BinaryEdge.io API Key.
- `cve_age_limit_days` — Ignore any vulnerability records older than this many days. 0 = unlimited.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxpages` — Maximum number of pages to iterate through, to avoid exceeding BinaryEdge API usage limits. APIv2 has a maximum of 500 pages (10,000 results).
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `port_age_limit_days` — Ignore any discovered open ports/banners older than this many days. 0 = unlimited.
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `torrent_age_limit_days` — Ignore any torrent records older than this many days. 0 = unlimited.
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Catalogue notes

We scan the entire public internet, create real-time threat intelligence streams, and reports that show the exposure of what is connected to the Internet.
We have built a distributed platform of scanners and honeypots, to acquire, classify and correlate different types of data.
We use all of these datapoints to match those digital assets to an organization, allowing us to provide a global, up-to-date, view of organizations known and unknown assets.
