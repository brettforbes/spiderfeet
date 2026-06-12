# sfp_alienvault

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** AlienVault OTX
- **service_origin:** `external-api`
- **Summary:** Obtain information from AlienVault Open Threat Exchange (OTX)

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `AFFILIATE_IPADDR` | ENTITY | yes |
| `AFFILIATE_IPV6_ADDRESS` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `IPV6_ADDRESS`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `NETBLOCK_MEMBER`, `NETBLOCKV6_MEMBER`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.urlFQDN`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_alienvault.py`
