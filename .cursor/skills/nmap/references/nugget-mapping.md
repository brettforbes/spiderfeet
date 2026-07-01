# Nmap XML → SpiderFeet Nugget Mapping

> **CLI profiling corpus (canonical V2 hierarchy):** use `.seed/scripts/cli_corpus/nmap_xml_to_graph.py`, structure doc [nmap_nugget_graph_structure.md](../../../.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md), and combined ontology [_Current_Ontology.md](../../../.docs/docs-for-cli-tools/_Current_Ontology.md). The sections below retain the **legacy flat** mapping used by `modules/sfp_tool_nmap.py` text/XML paths.

Convert **only** `-oX` XML into nugget **nodes** and **edges**. Catalogue: `.docs/analysis/nuggets.json` + `.docs/analysis/nuggets_extension.json`.

## V2 hierarchy mapping (CLI profiling)

| XML path | Nugget | Relation |
|----------|--------|----------|
| `nmaprun` scan head | `SCAN_RECORD` + `SCAN_*` descriptors | `had` |
| `host` + addresses | `HOST` → `NETWORKS` → `IP_ADDRESS` | `contains` |
| `port` | `TRANSPORT` → `PORT` + `PORT_STATE`, `PORT_PROTOCOL` | `contains` / `had` |
| `service@name` | `SERVICE` under `APPLICATIONS` | `contains`; **`listens-to` → `PORT`** (all reported services) |
| `service@product` + `@version` | `SERVICE_VERSION` | `SERVICE` → `had` |
| `service@servicefp` | `SERVICE_FINGERPRINT` | `SERVICE` → `had` |
| `service@extrainfo` | `SERVICE_EXTRAINFO` | `SERVICE` → `had` |
| `service/cpe` | `CPE_URL` | `SERVICE` → `contains` |
| `script ssh-hostkey` | `RSA` / `ECDSA` / … + key descriptors | `SERVICE` → `contains` |
| `os/osmatch` | `OPERATING_SYSTEM` + `OS_MATCH_ACCURACY` | `ENVIRONMENT` branch |
| `trace/hop` | `TRACE` → `TRACE_HOP` → hop `HOST` | `contains` |

Relations: `contains`, `had`, `listens-to` only (not `discovered`, `listens_on`, `runs`).

---

## Legacy flat mapping (module compatibility)

### Node shape (convention)

```python
{
    "id": "ip:203.0.113.10",
    "type": "IP_ADDRESS",
    "data": "203.0.113.10",
    "source_module": "sfp_tool_nmap",
    "provenance": {"xml": "scan.xml", "nmaprun@args": "..."}
}
```

```python
{
    "id": "tcp:203.0.113.10:443",
    "type": "TCP_PORT_OPEN",
    "data": "203.0.113.10:443",
}
```

## Edge shape

```python
{"source": "seed:example.com", "target": "ip:203.0.113.10", "relation": "discovered"}
{"source": "ip:203.0.113.10", "target": "tcp:203.0.113.10:443", "relation": "listens_on"}
```

## Primary mapping table

| XML location | Condition | Nugget type | `data` field |
|--------------|-----------|-------------|--------------|
| `host/status@state=up` + `address@ipv4` | host up | `IP_ADDRESS` | IPv4 string |
| `host/status@state=up` + `address@ipv6` | host up | `IP_ADDRESS` | IPv6 string |
| `address@mac` | present | `MAC_ADDRESS` | MAC (if in catalogue) or custom attribute on IP node |
| `hostname@name` | type PTR/user | `INTERNET_NAME` | FQDN |
| `port/state@state=open` + tcp | confirmed open | `TCP_PORT_OPEN` | `ip:port` |
| `port/state@state=open` + udp | confirmed open | `UDP_PORT_OPEN` | `ip:port` |
| `service@product` or `product`+`version` | on open port | `SOFTWARE_USED` | e.g. `OpenSSH 8.9p1` |
| `service@extrainfo` | banner fragment | `TCP_PORT_OPEN_BANNER` or `UDP_PORT_OPEN_INFO` | extrainfo text |
| `service` tunnel ssl | ssl service | `WEBSERVER_BANNER` / TLS attrs | from NSE `ssl-cert` preferred |
| `os/osmatch@name` | accuracy ≥ threshold | `OPERATING_SYSTEM` | match name |
| `os/osclass` | no osmatch | `OPERATING_SYSTEM` | `vendor osfamily osgen` joined |
| `hostscript/script` | smb-os, etc. | `OPERATING_SYSTEM` | parsed `elem` or output |
| `port/script` http-title | | `WEBSERVER_BANNER` | title string |
| `port/script` ssl-cert | | `SSL_CERTIFICATE_*` / custom | map per module spec |
| `distance@value` | traceroute | attribute on IP | hop count |
| `service/cpe` | CPE URI | link to vuln enrichment | optional node |

## State values — emit or skip

| `port/state@state` | Emit port nugget? |
|--------------------|-------------------|
| `open` | **Yes** |
| `closed` | No (unless inventory mode) |
| `filtered` | No; log as attribute `filtered_count` |
| `open\|filtered` | Policy: skip or emit with `confidence: low` |
| `closed\|filtered` | No |

## OS confidence policy

```python
OS_ACCURACY_MIN = 90

def os_from_host(host) -> str | None:
    os_el = host.find("os")
    if os_el is None:
        return None
    matches = sorted(
        os_el.findall("osmatch"),
        key=lambda m: int(m.get("accuracy", "0")),
        reverse=True,
    )
    for m in matches:
        if int(m.get("accuracy", "0")) >= OS_ACCURACY_MIN:
            return m.get("name")
    return None
```

Fallback order: `osmatch` → `osclass` from best match → NSE `smb-os-discovery` → `service@ostype`.

## Service string assembly

```python
def service_label(svc) -> str | None:
    if svc is None:
        return None
    parts = [svc.get("product"), svc.get("version"), svc.get("extrainfo")]
    label = " ".join(p for p in parts if p)
    if not label:
        return svc.get("name")
    return label.strip()
```

Emit `SOFTWARE_USED` when `product` or (`name` and `method=probed`).

## Hostname handling

```python
for hn in host.findall(".//hostname"):
    name = hn.get("name")
    htype = hn.get("type")
    # INTERNET_NAME node; edge ip -> name (relation: resolves_to / has_ptr)
```

Deduplicate: one `INTERNET_NAME` per FQDN.

## NSE script mapping (selected)

| Script id | Nugget / action |
|-----------|-----------------|
| `http-title` | `WEBSERVER_BANNER` — title text |
| `http-server-header` | `WEBSERVER_BANNER` |
| `ssl-cert` | certificate subject, SANs → `INTERNET_NAME` |
| `banner` | `TCP_PORT_OPEN_BANNER` |
| `smb-os-discovery` | `OPERATING_SYSTEM` |
| `ssh-hostkey` | fingerprint as attribute on port |
| `vulners` / `vuln` | route to vuln nuggets per module policy |

Parse structured `elem`/`table` children before regex on `output` attribute.

## Full parser skeleton

```python
import xml.etree.ElementTree as ET

def nmap_xml_to_nuggets(xml_path: str, seed_id: str) -> tuple[list, list]:
    root = ET.parse(xml_path).getroot()
    nodes, edges = [], []
    seen = set()

    def add_node(nid, ntype, data, **extra):
        if nid in seen:
            return
        seen.add(nid)
        nodes.append({"id": nid, "type": ntype, "data": data, **extra})

    def add_edge(src, tgt, relation):
        edges.append({"source": src, "target": tgt, "relation": relation})

    for host in root.findall("host"):
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue

        ip = None
        for addr in host.findall("address"):
            if addr.get("addrtype") in ("ipv4", "ipv6"):
                ip = addr.get("addr")
                break
        if not ip:
            continue

        ip_id = f"ip:{ip}"
        add_node(ip_id, "IP_ADDRESS", ip)
        add_edge(seed_id, ip_id, "discovered")

        for hn in host.findall(".//hostname"):
            name = hn.get("name")
            if name:
                hn_id = f"name:{name}"
                add_node(hn_id, "INTERNET_NAME", name)
                add_edge(ip_id, hn_id, "has_hostname")

        for port in host.findall(".//port"):
            st = port.find("state")
            if st is None or st.get("state") != "open":
                continue
            proto = port.get("protocol")
            portid = port.get("portid")
            if proto == "tcp":
                ptype = "TCP_PORT_OPEN"
            elif proto == "udp":
                ptype = "UDP_PORT_OPEN"
            else:
                continue
            pid = f"{proto}:{ip}:{portid}"
            add_node(pid, ptype, f"{ip}:{portid}")
            add_edge(ip_id, pid, "listens_on")

            svc = port.find("service")
            label = service_label(svc)
            if label:
                sw_id = f"software:{ip}:{portid}:{hash(label)}"
                add_node(sw_id, "SOFTWARE_USED", label)
                add_edge(pid, sw_id, "runs")

        os_name = os_from_host(host)
        if os_name:
            os_id = f"os:{ip}:{hash(os_name)}"
            add_node(os_id, "OPERATING_SYSTEM", os_name)
            add_edge(ip_id, os_id, "runs")

    return nodes, edges
```

## Legacy module note

`modules/sfp_tool_nmap.py` parses **text** lines (`OS details:`) from `-O` stdout. New implementations should:

1. Run with `-oX`.
2. Use this mapping.
3. Emit the same nugget types for compatibility.

## Deduplication and merges

- Key `TCP_PORT_OPEN` by `ip:port` string (SpiderFeet convention).
- Re-scan same target: merge nodes by `id`; append provenance list.
- Multiple `nmaprun` files: parse each; single graph reducer.

## Tests and fixtures

Store minimal XML fixtures under `test/fixtures/nmap/` with:

- single host open ports
- filtered host
- OS match block
- NSE script block

Assert nugget counts and types, not raw XML round-trip.
