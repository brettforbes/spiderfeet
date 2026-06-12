# sfp_pgp

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** PGP Key Servers
- **service_origin:** `local`
- **Summary:** Look up domains and e-mail addresses in PGP public key servers.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `AFFILIATE_EMAILADDR` | ENTITY | declared only |
| `PGP_KEY` | DATA | yes |

## Consumed nugget types

`INTERNET_NAME`, `EMAILADDR`, `DOMAIN_NAME`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `helpers.extractEmailsFromText`
- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_pgp.py`
