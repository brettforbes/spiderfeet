# sfp_tool_wafw00f

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - WAFW00F
- **service_origin:** `cli`
- **Summary:** Identify what web application firewall (WAF) is in use on the specified website.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

subprocess/Popen, json.loads

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_wafw00f.py`
