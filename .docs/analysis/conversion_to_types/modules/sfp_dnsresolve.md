# sfp_dnsresolve

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** DNS Resolver
- **service_origin:** `local`
- **Summary:** Resolves hosts and IP addresses identified, also extracted from raw content.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_IPADDR` | ENTITY | yes |
| `AFFILIATE_IPV6_ADDRESS` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `INTERNAL_IP_ADDRESS` | ENTITY | declared only |
| `DOMAIN_NAME_PARENT` | ENTITY | yes |
| `CO_HOSTED_SITE_DOMAIN` | ENTITY | declared only |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |

## Consumed nugget types

`CO_HOSTED_SITE`, `AFFILIATE_INTERNET_NAME`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `IP_ADDRESS`, `IPV6_ADDRESS`, `INTERNET_NAME`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `TARGET_WEB_CONTENT`, `BASE64_DATA`, `AFFILIATE_DOMAIN_WHOIS`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `LEAKSITE_CONTENT`, `RAW_DNS_RECORDS`, `RAW_FILE_META_DATA`, `RAW_RIR_DATA`, `SIMILARDOMAIN_WHOIS`, `SSL_CERTIFICATE_RAW`, `SSL_CERTIFICATE_ISSUED`, `TCP_PORT_OPEN_BANNER`, `WEBSERVER_BANNER`, `WEBSERVER_HTTPHEADERS`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.hostDomain`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.resolveIP`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnsresolve.py`
