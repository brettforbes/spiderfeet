# uncover Output and Parsing

Normalize records into canonical host and host:port entities.

## Parsing Steps

1. Parse record line/object.
2. Extract host/ip, port, provider, and evidence.
3. Normalize host casing and IP formatting.
4. Merge duplicates.
5. Emit nodes and edges with provider metadata.

## Python Skeleton

```python
nodes, edges = {}, []
for rec in records:
    host = (rec.get("host") or rec.get("ip") or "").strip().lower()
    port = rec.get("port")
    provider = rec.get("provider") or rec.get("source")
    if not host:
        continue
    hid = f"host:{host}"
    nodes.setdefault(hid, {"id": hid, "type": "INTERNET_NAME", "data": {"value": host}})
    if port:
        pid = f"port:{host}:{port}"
        nodes.setdefault(pid, {"id": pid, "type": "TCP_PORT_OPEN", "data": {"value": str(port)}})
        edges.append({"source": hid, "target": pid, "type": "HAS_OPEN_PORT", "data": {"provider": provider}})
```
