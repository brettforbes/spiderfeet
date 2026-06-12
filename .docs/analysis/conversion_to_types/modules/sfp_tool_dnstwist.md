# sfp_tool_dnstwist

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - DNSTwist
- **service_origin:** `cli`
- **Summary:** Identify bit-squatting, typo and other similar domains to the target using a local DNSTwist installation.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `SIMILARDOMAIN` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

subprocess/Popen, json.loads

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_dnstwist.py`
