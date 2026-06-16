# Katana Output and Parsing

Use JSONL output for reliable ingestion.

## Parsing Rules

1. Read one line at a time.
2. Trim whitespace.
3. Skip empty/non-JSON lines.
4. Parse JSON with exception handling.
5. Extract URL and host.
6. Emit/merge nodes and provenance edges.

## Python Skeleton

```python
import json
from urllib.parse import urlparse

nodes, edges = {}, []
for raw in lines:
    line = raw.strip()
    if not line or not line.startswith("{"):
        continue
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    url = obj.get("url")
    if not url:
        continue
    host = urlparse(url).hostname
    uid = f"url:{url}"
    nodes.setdefault(uid, {"id": uid, "type": "URL", "data": {"value": url}})
    if host:
        hid = f"host:{host}"
        nodes.setdefault(hid, {"id": hid, "type": "INTERNET_NAME", "data": {"value": host}})
        edges.append({"source": hid, "target": uid, "type": "DISCOVERED_URL"})
```
