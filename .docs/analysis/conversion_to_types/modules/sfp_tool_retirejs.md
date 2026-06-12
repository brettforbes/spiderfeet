# sfp_tool_retirejs

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - Retire.js
- **service_origin:** `cli`
- **Summary:** Scanner detecting the use of JavaScript libraries with known vulnerabilities

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`

## Parsing signals (static)

subprocess/Popen, json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.cveInfo`
- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_retirejs.py`
