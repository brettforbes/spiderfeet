# sfp_intfiles

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Interesting File Finder
- **service_origin:** `local`
- **Summary:** Identifies potential files of interest, e.g. office documents, zip files.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERESTING_FILE` | DESCRIPTOR | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`

## Parsing signals (static)

_(none detected)_

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_intfiles.py`
