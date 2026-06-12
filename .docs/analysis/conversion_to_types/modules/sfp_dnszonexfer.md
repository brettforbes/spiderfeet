# sfp_dnszonexfer

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** DNS Zone Transfer
- **service_origin:** `local`
- **Summary:** Attempts to perform a full DNS zone transfer.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_DNS_RECORDS` | DATA | yes |
| `INTERNET_NAME` | ENTITY | yes |

## Consumed nugget types

`PROVIDER_DNS`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.resolveHost`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnszonexfer.py`
