# sfp_webserver

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Web Server Identifier
- **service_origin:** `local`
- **Summary:** Obtain web server banners to identify versions of web servers being used.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WEBSERVER_BANNER` | DATA | yes |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `LINKED_URL_EXTERNAL` | SUBENTITY | yes |

## Consumed nugget types

`WEBSERVER_HTTPHEADERS`

## Parsing signals (static)

json.loads

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_webserver.py`
