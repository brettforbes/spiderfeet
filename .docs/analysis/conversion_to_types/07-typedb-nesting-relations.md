# TypeDB nesting relations (planned)

Today the map schema (`/.seed/spiderfeet_map.tql`) models **archetypes** (nugget entity subtypes) and **routes** between types at the OSINT-service level. **Scan instances** store flat `nugget_data` strings. Nesting (system → IPs → ports) is implied by provenance chains and string encoding (`ip:port`), not queryable structure.

This document proposes **instance-level relations** for infrastructure findings — the natural graph for internal/external scanning.

---

## Use cases

1. Domain `example.com` resolves to hosts; each host has one or more IPs; each IP has open ports; ports have banners and detected services.
2. Nuclei/nmap findings attach to the **port** or **host**, not only to a flat event list.
3. UI force graph can collapse/expand hierarchy without re-parsing strings.

---

## Proposed entity instances (beyond `nugget`)

Keep existing `nugget` instances for backward compatibility. Add **typed instance entities** when structured payload is available:

| Entity | Key attributes | Notes |
|--------|----------------|-------|
| `host` | `hostname`, `fqdn` | From `INTERNET_NAME` |
| `ip-endpoint` | `address`, `version` | From `IP_ADDRESS` / `IPV6_ADDRESS` |
| `transport-endpoint` | `ip`, `port`, `protocol` | Normalised port observation |
| `network-service` | `name`, `product`, `version` | From banners, WhatWeb, nuclei |
| `vulnerability` | `cve_id`, `severity` | From CVE tier types |

These can be **subtypes of `nugget`** or linked via relations — recommendation: **link** so existing map routes unchanged.

---

## Proposed relations

```typeql
# Logical names — kebab-case per project convention

relation host-resolution,
  relates resolved-host,
  relates resolved-ip;

relation host-address,
  relates owning-host,
  relates host-ip;

relation listening-service,
  relates service-endpoint,  # transport-endpoint
  relates network-service;

relation endpoint-banner,
  relates service-endpoint,
  relates banner-text;       # or descriptor nugget

relation service-vulnerability,
  relates affected-endpoint,
  relates vulnerability;

relation scan-discovery,
  relates scan-record,
  relates discovered-entity;
```

### Example graph

```
(domain-name nugget: example.com)
    └── host-resolution ──> (host: www.example.com)
            └── host-address ──> (ip-endpoint: 93.184.216.34)
                    └── listening-service ──> (transport-endpoint: :443/tcp)
                            ├── endpoint-banner ──> "HTTP/1.1 ..."
                            └── service-vulnerability ──> (vulnerability: CVE-…)
```

---

## Mapping from SpiderFeet events

| Event type | Current `data` | Structured extraction | Relations |
|------------|----------------|----------------------|-----------|
| `INTERNET_NAME` | hostname | `{ "hostname": "..." }` | `host` instance |
| `IP_ADDRESS` | ip | `{ "address": "..." }` | `ip-endpoint`; link to parent host if source was name |
| `TCP_PORT_OPEN` | `ip:port` | split on `:` | `transport-endpoint`; `listening-service` |
| `TCP_PORT_OPEN_BANNER` | banner text | link via sourceEvent port | `endpoint-banner` |
| `OPERATING_SYSTEM` | OS string | parse or attach to host | attribute on `host` or descriptor |
| `VULNERABILITY_CVE_*` | CVE text | `sf.cveInfo` metadata | `vulnerability` + `service-vulnerability` |
| `WEBSERVER_TECHNOLOGY` | product string | `{ "product": "..." }` | `network-service` |

**Ingest rule:** When `sourceEvent` chain is `DOMAIN → INTERNET_NAME → IP_ADDRESS → TCP_PORT_OPEN`, create resolution + address + listening-service relations in one transaction.

---

## TypeQL sketch (illustrative)

```typeql
entity host @abstract,
  owns hostname @key,
  plays host-resolution:resolved-host,
  plays host-address:owning-host;

entity internet-name sub host;

entity ip-endpoint,
  owns address @key,
  owns ip-version,
  plays host-resolution:resolved-ip,
  plays host-address:host-ip,
  plays listening-service:service-endpoint;

entity transport-endpoint sub ip-endpoint,
  owns port,
  owns protocol;

relation host-resolution sub association,
  relates resolved-host,
  relates resolved-ip;

relation listening-service sub association,
  relates service-endpoint,
  relates network-service;
```

(Full schema merge with existing `nugget` hierarchy is a governed change — bind to SPEC-002 / Stage 6 storage epic.)

---

## Migration strategy

1. **Read-only projection** — Post-scan job parses existing flat events into relations; no module changes.
2. **Dual write** — Modules emit structured payload; ingest writes both flat nugget + relations.
3. **UI cutover** — Maps tab queries relations for expand/collapse; flat list remains for Logs/Tests.

---

## Query examples (target)

```typeql
match
  $h isa internet-name, has hostname "www.example.com";
  $r (resolved-host: $h, resolved-ip: $ip) isa host-resolution;
  $p (service-endpoint: $ep) isa listening-service;
  $ep has address "93.184.216.34", has port 443;
fetch { $h, $ip, $ep };
```

```typeql
# All critical CVEs on ports discovered in scan S
match
  $scan isa scan-record, has scan_id "…";
  $d (scan-record: $scan, discovered-entity: $v) isa scan-discovery;
  $v isa vulnerability, has severity "critical";
fetch { $v };
```

---

## Dependencies

- [06-recommendations-and-roadmap.md](06-recommendations-and-roadmap.md) Phase C (structured payload)
- TypeDB bridge skill for insert patterns
- Map bootstrap update after schema amendment

---

## Non-goals (initial slice)

- Full OSINT entity model (emails, breaches) — add relations incrementally
- Replacing `nugget` archetype catalogue — extend, don’t fork
- Real-time streaming ingest during scan (batch post-scan is acceptable first)
