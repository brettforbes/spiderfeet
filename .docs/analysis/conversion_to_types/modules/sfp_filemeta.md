# sfp_filemeta

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** File Metadata Extractor
- **service_origin:** `local`
- **Summary:** Extracts meta data from documents and images.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_FILE_META_DATA` | DATA | yes |
| `SOFTWARE_USED` | SUBENTITY | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`, `INTERESTING_FILE`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_filemeta.py`
