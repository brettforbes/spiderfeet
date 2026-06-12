# sfp_email

**Conversion pattern:** `content_extract` — Parses page/content events with helpers/regex; emits derived identifiers.

## Catalogue

- **Name:** E-Mail Address Extractor
- **service_origin:** `local`
- **Summary:** Identify e-mail addresses in any obtained data.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `AFFILIATE_EMAILADDR` | ENTITY | declared only |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `BASE64_DATA`, `AFFILIATE_DOMAIN_WHOIS`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `LEAKSITE_CONTENT`, `RAW_DNS_RECORDS`, `RAW_FILE_META_DATA`, `RAW_RIR_DATA`, `SIMILARDOMAIN_WHOIS`, `SSL_CERTIFICATE_RAW`, `SSL_CERTIFICATE_ISSUED`, `TCP_PORT_OPEN_BANNER`, `WEBSERVER_BANNER`, `WEBSERVER_HTTPHEADERS`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `helpers.extractEmailsFromText`
- `sf.validHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_email.py`
