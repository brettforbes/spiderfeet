# sfp_adblock

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** AdBlock Check
- **service_origin:** `external-api`
- **Summary:** Check if linked pages would be blocked by AdBlock Plus.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `URL_ADBLOCKED_INTERNAL` | DESCRIPTOR | yes |
| `URL_ADBLOCKED_EXTERNAL` | DESCRIPTOR | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`, `PROVIDER_JAVASCRIPT`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_adblock.py`
