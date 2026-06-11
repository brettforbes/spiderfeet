# Tool - Nuclei

**Module ID:** `sfp_tool_nuclei`

## Summary

Fast and customisable vulnerability scanner.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_nuclei
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_nuclei

## CLI / tool

- **Tool:** Nuclei
- **Website:** https://nuclei.projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/nuclei

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`
- `IP_ADDRESS`
- `VULNERABILITY_GENERAL`
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** tool, slow, invasive
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `netblockscan` — Check all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `nuclei_path` — The path to your nuclei binary. Must be set.
- `template_path` — The path to your nuclei templates. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=29

## Catalogue notes

Fast and customisable vulnerability scanner.

**Module ID:** `sfp_tool_nuclei`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, IP_ADDRESS, NETBLOCK_OWNER
**Produces:** VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, IP_ADDRESS, VULNERABILITY_GENERAL, WEBSERVER_TECHNOLOGY
**Flags:** tool, slow, invasive

**Tool requirement:**
Install ProjectDiscovery Nuclei; `nuclei` on PATH.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
