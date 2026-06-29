# Julius JSON / JSONL Output Schema

Agents should use **`julius probe -o jsonl`** (or `-o json` for small batches).

## JSON array mode (`-o json`)

Top-level **array** of result objects:

```json
[
  {
    "target": "https://target.example.com/api/tags",
    "service": "ollama",
    "matched_request": "/api/tags",
    "category": "self-hosted",
    "specificity": 100,
    "models": ["llama2", "mistral"]
  }
]
```

## JSON Lines mode (`-o jsonl`)

One **JSON object per line** (NDJSON). Parse line-by-line; skip empty lines.

Same fields as array elements.

## Result object fields

| Field | Type | Always | Description |
|-------|------|--------|-------------|
| `target` | string | yes | Normalized URL of matched request (may include path) |
| `service` | string | yes | Probe name / service id (e.g. `ollama`, `vllm`, `openai-compatible`) |
| `matched_request` | string | yes | Request path that matched (e.g. `/api/tags`) |
| `category` | string | yes | `self-hosted`, `gateway`, `rag-orchestration`, `cloud-managed`, `generic` |
| `specificity` | int | yes | 1–100; higher = more confident identification |
| `models` | string[] | no | Extracted model names when probe supports model JQ extraction |
| `generator_configs` | object[] | no | Present when `--augustus` and probe defines Augustus config |
| `error` | string | no | HTTP or probe error for this attempt |

## Table columns (human `-o table`)

TARGET | SERVICE | SPECIFICITY | CATEGORY | MODELS | ERROR

## Parsing rules

1. **Multiple matches per target** — Julius sorts by specificity (highest first). For nuggets, prefer highest-specificity row per base host unless operator wants full enumeration.
2. **`openai-compatible` at specificity 1** — fallback only; treat as low confidence unless no other match.
3. **`error` non-empty** — do not emit `SOFTWARE_USED` from that row; log as scan error nugget if policy requires.
4. **Extract host/port** from `target` URL for linking to prior `TCP_PORT_OPEN` from Naabu/Nmap.
5. **`models` array** — emit child `SOFTWARE_USED` or `DESCRIPTION_ABSTRACT` nodes per model name (see nugget-mapping.md).

## Python parse sketch

```python
import json
from urllib.parse import urlparse

def iter_julius_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)

for row in iter_julius_jsonl("julius.jsonl"):
    parsed = urlparse(row["target"])
    print(parsed.hostname, parsed.port, row["service"], row.get("models"))
```
