# sfp_tool_nuclei

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - Nuclei
- **service_origin:** `cli`
- **Summary:** Fast and customisable vulnerability scanner.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |
| `IP_ADDRESS` | ENTITY | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | declared only |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | declared only |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

subprocess/Popen, json.loads, regex

**SpiderFeet/sf helpers used:**

- `sf.cveInfo`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_nuclei.py`
