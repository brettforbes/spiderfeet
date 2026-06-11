# Tool - nbtscan

**Module ID:** `sfp_tool_nbtscan`

## Summary

Scans for open NETBIOS nameservers on your target's network.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_nbtscan
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_nbtscan

## CLI / tool

- **Tool:** nbtscan
- **Website:** http://www.unixwiz.net/tools/nbtscan.html
- **Repository:** http://www.unixwiz.net/tools/nbtscan.html

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `UDP_PORT_OPEN`
- `UDP_PORT_OPEN_INFO`
- `IP_ADDRESS`

## Flags and categories

- **Flags:** tool, slow
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `nbtscan_path` — The path to your nbtscan binary
- `netblockscan` — Scan all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)

## Test seeds

- `IP_ADDRESS`: input=`127.0.0.1` validation=smoke smoke

## Catalogue notes

Scans for open NETBIOS nameservers on your target's network.

**Module ID:** `sfp_tool_nbtscan`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS, NETBLOCK_OWNER
**Produces:** UDP_PORT_OPEN, UDP_PORT_OPEN_INFO, IP_ADDRESS
**Flags:** tool, slow

**Tool requirement:**
Install nbtscan.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `IP_ADDRESS`
- Input: `127.0.0.1`
- Produced count: 0
