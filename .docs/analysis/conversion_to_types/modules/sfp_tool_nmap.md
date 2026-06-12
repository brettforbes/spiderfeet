# sfp_tool_nmap

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - Nmap
- **service_origin:** `cli`
- **Summary:** Identify what Operating System might be used.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `IP_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

subprocess/Popen

**SpiderFeet/sf helpers used:**

- `sf.validIP`
- `sf.validIpNetwork`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_nmap.py`
