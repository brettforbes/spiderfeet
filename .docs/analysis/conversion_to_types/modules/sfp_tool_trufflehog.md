# sfp_tool_trufflehog

**Conversion pattern:** `cli_subprocess_parse` — Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.

## Catalogue

- **Name:** Tool - TruffleHog
- **service_origin:** `cli`
- **Summary:** Searches through git repositories for high entropy strings and secrets, digging deep into commit history.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `PASSWORD_COMPROMISED` | DATA | yes |

## Consumed nugget types

`SOCIAL_MEDIA`, `PUBLIC_CODE_REPO`

## Parsing signals (static)

subprocess/Popen, json.loads

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_tool_trufflehog.py`
