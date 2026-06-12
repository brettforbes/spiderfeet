# sfp_pageinfo

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Page Information
- **service_origin:** `local`
- **Summary:** Obtain information about web pages (do they take passwords, do they contain forms, etc.)

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `URL_STATIC` | DESCRIPTOR | yes |
| `URL_JAVASCRIPT` | DESCRIPTOR | declared only |
| `URL_FORM` | DESCRIPTOR | declared only |
| `URL_PASSWORD` | DESCRIPTOR | declared only |
| `URL_UPLOAD` | DESCRIPTOR | declared only |
| `URL_JAVA_APPLET` | DESCRIPTOR | declared only |
| `URL_FLASH` | DESCRIPTOR | declared only |
| `PROVIDER_JAVASCRIPT` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_pageinfo.py`
