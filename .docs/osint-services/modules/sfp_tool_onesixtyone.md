# Tool - onesixtyone

**Module ID:** `sfp_tool_onesixtyone`

## Summary

Fast scanner to find publicly exposed SNMP services.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_onesixtyone
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_onesixtyone

## CLI / tool

- **Tool:** onesixtyone
- **Website:** https://github.com/trailofbits/onesixtyone
- **Repository:** https://github.com/trailofbits/onesixtyone

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `UDP_PORT_OPEN_INFO`
- `UDP_PORT_OPEN`
- `IP_ADDRESS`

## Flags and categories

- **Flags:** tool
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `communities` — Comma-separated list of SNMP communities to try.
- `netblockscan` — Scan all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `onesixtyone_path` — The path to your onesixtyone binary. Must be set.

## Test seeds

- `IP_ADDRESS`: input=`127.0.0.1` validation=smoke smoke

## Catalogue notes

Fast scanner to find publicly exposed SNMP services.

**Module ID:** `sfp_tool_onesixtyone`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS, NETBLOCK_OWNER
**Produces:** UDP_PORT_OPEN_INFO, UDP_PORT_OPEN, IP_ADDRESS
**Flags:** tool

**Tool requirement:**
Install onesixtyone SNMP scanner.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `IP_ADDRESS`
- Input: `127.0.0.1`
- Produced count: 0
