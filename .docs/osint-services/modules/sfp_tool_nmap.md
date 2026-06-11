# Tool - Nmap

**Module ID:** `sfp_tool_nmap`

## Summary

Identify what Operating System might be used.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_nmap
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_nmap

## CLI / tool

- **Tool:** Nmap
- **Website:** https://nmap.org/
- **Repository:** https://svn.nmap.org/nmap

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `OPERATING_SYSTEM`
- `IP_ADDRESS`

## Flags and categories

- **Flags:** tool, slow, invasive
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `netblockscan` — Port scan all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `nmappath` — Path to the where the nmap binary lives. Must be set.

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke smoke

## Catalogue notes

Identify what Operating System might be used.

**Module ID:** `sfp_tool_nmap`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS, NETBLOCK_OWNER
**Produces:** OPERATING_SYSTEM, IP_ADDRESS
**Flags:** tool, slow, invasive

**Tool requirement:**
Install Nmap and ensure `nmap` is on PATH.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `IP_ADDRESS`
- Input: `127.0.0.1`
- Produced count: 0
