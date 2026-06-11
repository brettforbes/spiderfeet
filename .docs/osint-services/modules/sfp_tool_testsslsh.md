# Tool - testssl.sh

**Module ID:** `sfp_tool_testsslsh`

## Summary

Identify various TLS/SSL weaknesses, including Heartbleed, CRIME and ROBOT.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_testsslsh
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_testsslsh

## CLI / tool

- **Tool:** testssl.sh
- **Website:** https://testssl.sh
- **Repository:** https://github.com/drwetter/testssl.sh

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
- `VULNERABILITY_GENERAL`
- `IP_ADDRESS`

## Flags and categories

- **Flags:** tool
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `mincve` — Only report CVEs equal to or higher than this level, must be either LOW, MEDIUM, HIGH or CRITICAL.
- `netblockscan` — Test all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to test IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `testsslsh_path` — Path to your testssl.sh executable. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=5

## Catalogue notes

Identify various TLS/SSL weaknesses, including Heartbleed, CRIME and ROBOT.

**Module ID:** `sfp_tool_testsslsh`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME, IP_ADDRESS, NETBLOCK_OWNER
**Produces:** VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, VULNERABILITY_GENERAL, IP_ADDRESS
**Flags:** tool

**Tool requirement:**
Install testssl.sh and OpenSSL dependencies.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
