# sfp_tool_onesixtyone

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - onesixtyone
- **service_origin:** `cli`
- **Summary:** Fast scanner to find publicly exposed SNMP services.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `UDP_PORT_OPEN_INFO` | DATA | yes |
| `UDP_PORT_OPEN` | SUBENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

subprocess/Popen

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_onesixtyone.py`
