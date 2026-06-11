# Port Scanner - TCP

**Module ID:** `sfp_portscan_tcp`

## Summary

Scans for commonly open TCP ports on Internet-facing systems.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_portscan_tcp
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_portscan_tcp

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `NETBLOCK_OWNER`
- **Produced:**
- `TCP_PORT_OPEN`
- `TCP_PORT_OPEN_BANNER`

## Flags and categories

- **Flags:** slow, invasive
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `maxthreads` — Number of ports to try to open simultaneously (number of threads to spawn at once.)
- `netblockscan` — Port scan all IPs within identified owned netblocks?
- `netblockscanmax` — Maximum netblock/subnet size to scan IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `ports` — The TCP ports to scan. Prefix with an '@' to iterate through a file containing ports to try (one per line), e.g. @C:\ports.txt or @/home/bob/ports.txt. Or supply a URL to load the list from there.
- `randomize` — Randomize the order of ports scanned.
- `timeout` — Seconds before giving up on a port.

## Test seeds

- `IP_ADDRESS`: input=`127.0.0.1` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Scans for commonly open TCP ports on Internet-facing systems.

**Module ID:** `sfp_portscan_tcp`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** IP_ADDRESS, NETBLOCK_OWNER
**Produces:** TCP_PORT_OPEN, TCP_PORT_OPEN_BANNER
**Flags:** slow, invasive

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `IP_ADDRESS`
- Input: `127.0.0.1`
- Produced count: 1
