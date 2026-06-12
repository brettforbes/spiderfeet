# sfp_tool_cmseek

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - CMSeeK
- **service_origin:** `cli`
- **Summary:** Identify what Content Management System (CMS) might be used.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

subprocess/Popen, json.loads

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_cmseek.py`
