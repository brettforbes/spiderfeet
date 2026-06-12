# sfp_strangeheaders

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Strange Header Identifier
- **service_origin:** `local`
- **Summary:** Obtain non-standard HTTP headers returned by web servers.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WEBSERVER_STRANGEHEADER` | DATA | yes |

## Consumed nugget types

`WEBSERVER_HTTPHEADERS`

## Parsing signals (static)

json.loads

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_strangeheaders.py`
