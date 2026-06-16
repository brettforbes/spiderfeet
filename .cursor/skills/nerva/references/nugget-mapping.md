# Nerva → Nugget Mapping

Nerva `--json` lines map to **port**, **service**, and **banner/metadata** nuggets linked to parent `IP_ADDRESS` hosts from upstream discovery (netdiscover/Nmap).

## Input record

```json
{
  "host": "192.168.1.100",
  "ip": "192.168.1.100",
  "port": 22,
  "protocol": "ssh",
  "transport": "tcp",
  "metadata": {
    "banner": "SSH-2.0-OpenSSH_8.9p1"
  }
}
```

## Target nugget types

| JSON field | SpiderFeet event / nugget | Notes |
|------------|---------------------------|-------|
| `ip` + `port` + `transport` | `TCP_PORT_OPEN` or `UDP_PORT_OPEN` | `data` = `{ip}:{port}` |
| `protocol` | attribute or `SERVICE` / `SOFTWARE_USED` | Service slug |
| `metadata.banner` | `TCP_PORT_OPEN_BANNER` | When banner present |
| `metadata.version` | `SOFTWARE_USED` | Version string |
| `metadata.technologies` | web stack nuggets | HTTP plugins |
| `host` (if FQDN) | `INTERNET_NAME` | When host ≠ ip |
| Full record | provenance blob | Audit trail |

See `.docs/analysis/nuggets.json` for canonical vocabulary.

## Graph shape

```
IP_ADDRESS (from netdiscover/nmap)
  └─ listens_on → TCP_PORT_OPEN / UDP_PORT_OPEN
        └─ runs_service → protocol nugget
        └─ banner → TCP_PORT_OPEN_BANNER (if metadata.banner)
        └─ metadata → RAW_RIR_DATA or attributes
```

## Python mapping

```python
import json

def port_event_type(transport: str) -> str:
    return "UDP_PORT_OPEN" if transport == "udp" else "TCP_PORT_OPEN"

def to_nodes_edges(records: list[dict], parent_ip_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    seen = set()

    def add(node_id, ntype, data, attrs=None):
        if node_id in seen:
            return
        seen.add(node_id)
        n = {"id": node_id, "type": ntype, "data": data}
        if attrs:
            n["attributes"] = attrs
        nodes.append(n)

    for rec in records:
        ip = rec["ip"]
        port = rec["port"]
        transport = rec.get("transport", "tcp")
        protocol = rec.get("protocol", "unknown")
        host = rec.get("host", ip)
        meta = rec.get("metadata") or {}

        ip_id = f"ip:{ip}"
        port_data = f"{ip}:{port}"
        port_id = f"{transport}:{port_data}"
        svc_id = f"svc:{ip}:{port}:{protocol}"

        add(ip_id, "IP_ADDRESS", ip)
        add(port_id, port_event_type(transport), port_data, {"protocol": protocol})
        add(svc_id, "SOFTWARE_USED", protocol, {"transport": transport, "metadata": meta})

        edges.append({"source": parent_ip_id or ip_id, "target": ip_id, "relation": "discovered"})
        edges.append({"source": ip_id, "target": port_id, "relation": "listens_on"})
        edges.append({"source": port_id, "target": svc_id, "relation": "runs_service"})

        if host != ip:
            hn_id = f"name:{host}"
            add(hn_id, "INTERNET_NAME", host)
            edges.append({"source": ip_id, "target": hn_id, "relation": "resolved"})

        banner = meta.get("banner")
        if banner:
            b_id = f"banner:{ip}:{port}"
            add(b_id, "TCP_PORT_OPEN_BANNER", banner)
            edges.append({"source": port_id, "target": b_id, "relation": "banner"})

        for tech in meta.get("technologies") or []:
            t_id = f"tech:{tech}"
            add(t_id, "SOFTWARE_USED", tech)
            edges.append({"source": port_id, "target": t_id, "relation": "technology"})

    return nodes, edges


def parse_nerva_jsonl(raw: str) -> list[dict]:
    out = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out
```

## Module integration (`sfp_tool_nerva`)

Expected flow:

1. Receive `IP_ADDRESS` or `TCP_PORT_OPEN` parent event
2. Build `host:port` target list (from event or aggregated scan)
3. Run `nerva -l targets.txt --json`
4. Parse JSON lines (not human output)
5. Emit port and service events per record

```python
# subprocess
args = [exe, "-l", targets_file, "--json"]
# for each line in stdout: json.loads(line) → notifyListeners
```

## Linking to netdiscover upstream

| Stage | Nugget output |
|-------|---------------|
| netdiscover `-P` | `IP_ADDRESS`, `MAC_ADDRESS` |
| nmap | `TCP_PORT_OPEN` (discovery) |
| nerva `--json` | enriches with `protocol`, `metadata` |

Nerva **enriches** port nuggets — it does not replace netdiscover host discovery.

## Transport-specific handling

| `transport` | Event type | CLI flag used |
|---------------|------------|---------------|
| `tcp` | `TCP_PORT_OPEN` | default |
| `udp` | `UDP_PORT_OPEN` | `-U` |
| `sctp` | `TCP_PORT_OPEN`* | `-S` |

\*Map SCTP to project SCTP nugget type if defined; else `TCP_PORT_OPEN` with `attributes.transport=sctp`.

## Clean miss semantics

If nerva returns **no JSON line** for a target:

- Port may be closed, filtered, or unrecognized
- Stage 4 negative pass: `module_execution.verdict = clean_miss` when expected

Do not fabricate service nuggets without a JSON record.

## Provenance

```python
node["provenance"] = {
    "module": "sfp_tool_nerva",
    "tool": "nerva",
    "flags": "--json",
    "raw": rec,
}
```

## Cross-reference

- JSON schema: [`json-output-schema.md`](json-output-schema.md)
- Upstream host nuggets: [`../../netdiscover/references/nugget-mapping.md`](../../netdiscover/references/nugget-mapping.md)
- TextFSM (not used for nerva): use `json` module only
