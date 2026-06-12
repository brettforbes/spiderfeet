# sfp_callername

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** CallerName
- **service_origin:** `external-api`
- **Summary:** Lookup US phone number location and reputation information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | yes |
| `MALICIOUS_PHONE_NUMBER` | DESCRIPTOR | yes |

## Consumed nugget types

`PHONE_NUMBER`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_callername.py`
