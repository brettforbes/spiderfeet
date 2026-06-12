# sfp_tool_snallygaster

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - snallygaster
- **service_origin:** `cli`
- **Summary:** Finds file leaks and other security problems on HTTP servers.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `VULNERABILITY_GENERAL` | DESCRIPTOR | yes |
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

subprocess/Popen, json.loads

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_snallygaster.py`
