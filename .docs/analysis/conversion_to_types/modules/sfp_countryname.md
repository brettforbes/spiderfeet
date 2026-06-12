# sfp_countryname

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Country Name Extractor
- **service_origin:** `local`
- **Summary:** Identify country names in any obtained data.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `COUNTRY_NAME` | ENTITY | yes |

## Consumed nugget types

`IBAN_NUMBER`, `PHONE_NUMBER`, `AFFILIATE_DOMAIN_NAME`, `CO_HOSTED_SITE_DOMAIN`, `DOMAIN_NAME`, `SIMILARDOMAIN`, `AFFILIATE_DOMAIN_WHOIS`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, `DOMAIN_WHOIS`, `GEOINFO`, `PHYSICAL_ADDRESS`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_countryname.py`
