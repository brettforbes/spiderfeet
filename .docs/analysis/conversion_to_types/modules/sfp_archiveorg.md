# sfp_archiveorg

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Archive.org
- **service_origin:** `external-api`
- **Summary:** Identifies historic versions of interesting files/pages from the Wayback Machine.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERESTING_FILE_HISTORIC` | DESCRIPTOR | declared only |
| `URL_PASSWORD_HISTORIC` | DESCRIPTOR | declared only |
| `URL_FORM_HISTORIC` | DESCRIPTOR | declared only |
| `URL_FLASH_HISTORIC` | DESCRIPTOR | declared only |
| `URL_STATIC_HISTORIC` | DESCRIPTOR | declared only |
| `URL_JAVA_APPLET_HISTORIC` | DESCRIPTOR | declared only |
| `URL_UPLOAD_HISTORIC` | DESCRIPTOR | declared only |
| `URL_WEB_FRAMEWORK_HISTORIC` | DESCRIPTOR | declared only |
| `URL_JAVASCRIPT_HISTORIC` | DESCRIPTOR | declared only |

## Consumed nugget types

`INTERESTING_FILE`, `URL_PASSWORD`, `URL_FORM`, `URL_FLASH`, `URL_STATIC`, `URL_JAVA_APPLET`, `URL_UPLOAD`, `URL_JAVASCRIPT`, `URL_WEB_FRAMEWORK`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_archiveorg.py`
