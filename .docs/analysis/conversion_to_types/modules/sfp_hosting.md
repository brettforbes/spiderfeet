# sfp_hosting

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Hosting Provider Identifier
- **service_origin:** `local`
- **Summary:** Find out if any IP addresses identified fall within known 3rd party hosting ranges, e.g. Amazon, Azure, etc.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `PROVIDER_HOSTING` | ENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_hosting.py`
