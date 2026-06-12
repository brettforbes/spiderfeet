# sfp_creditcard

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Credit Card Number Extractor
- **service_origin:** `local`
- **Summary:** Identify Credit Card Numbers in any data

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CREDIT_CARD_NUMBER` | ENTITY | yes |

## Consumed nugget types

`DARKNET_MENTION_CONTENT`, `LEAKSITE_CONTENT`

## Parsing signals (static)

_(none detected)_

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_creditcard.py`
