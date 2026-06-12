# sfp_mnemonic

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Mnemonic PassiveDNS
- **service_origin:** `external-api`
- **Summary:** Obtain Passive DNS information from PassiveDNS.mnemonic.no.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `INTERNAL_IP_ADDRESS` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `INTERNET_NAME_UNRESOLVED`

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `INTERNET_NAME`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_mnemonic.py`
