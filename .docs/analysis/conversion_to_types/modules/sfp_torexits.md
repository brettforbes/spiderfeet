# sfp_torexits

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** TOR Exit Nodes
- **service_origin:** `external-api`
- **Summary:** Check if an IP adddress or netblock appears on the Tor Metrics exit node list.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `TOR_EXIT_NODE` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_torexits.py`
