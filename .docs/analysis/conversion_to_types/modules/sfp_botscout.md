# sfp_botscout

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** BotScout
- **service_origin:** `external-api`
- **Summary:** Searches BotScout.com's database of spam-bot IP addresses and e-mail addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `BLACKLISTED_IPADDR` | DESCRIPTOR | yes |
| `MALICIOUS_EMAILADDR` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `EMAILADDR`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_botscout.py`
