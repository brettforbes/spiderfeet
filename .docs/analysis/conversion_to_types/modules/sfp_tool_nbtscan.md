# sfp_tool_nbtscan

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - nbtscan
- **service_origin:** `cli`
- **Summary:** Scans for open NETBIOS nameservers on your target's network.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `UDP_PORT_OPEN` | SUBENTITY | yes |
| `UDP_PORT_OPEN_INFO` | DATA | yes |
| `IP_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

subprocess/Popen

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_nbtscan.py`
