# Julius JSON / JSONL Output Schema

Agents should use **`julius probe -o jsonl`** (streams / multi-target) or **`-o json`** (small batches, clean-miss `[]`).

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

**Clean miss (observed):** stdout `[]` with a human message such as `No match found for https://example.com` (may appear on stderr/stdout depending on capture). Empty array is a valid structured artifact.

## JSON Lines mode (`-o jsonl`)

One **JSON object per line** (NDJSON). Parse line-by-line; skip empty / non-JSON lines (banners).

Same object fields as array elements.

## Result object fields

| Field | Type | Always | Description |
|-------|------|--------|-------------|
| `target` | string | yes | Normalized URL of matched request (may include path) |
| `service` | string | yes | Probe name / service id (e.g. `ollama`, `vllm`, `openai-compatible`) |
| `matched_request` | string | yes | Request path that matched (e.g. `/api/tags`) |
| `category` | string | yes | e.g. `self-hosted`, `gateway`, `rag-orchestration`, `cloud-managed`, `mcp`, `generic` |
| `specificity` | int | yes | 1–100; higher = more confident identification |
| `models` | string[] | no | Extracted model names when probe supports model extraction |
| `generator_configs` | object[] | no | Present when `--augustus` and probe defines Augustus config |
| `error` | string | no | HTTP or probe error for this attempt |

## Table columns (human `-o table`)

TARGET | SERVICE | SPECIFICITY | CATEGORY | MODELS | ERROR

## Harvest / SpiderFeet bundle note

Do **not** store raw `.jsonl` as the CLI Profiling Structured pane file. At harvest, wrap JSONL into a single-root JSON bundle (`schema` + `records[]`) per proj-06; derive Text from `records[]`.

## Parsing rules

1. **Multiple matches per target** — prefer highest-specificity row per base host unless full enumeration is required.
2. **`openai-compatible` at specificity 1** — fallback only; low confidence.
3. **`error` non-empty** — do not emit service software nuggets from that row alone.
4. **Extract host/port** from `target` for linking to prior `TCP_PORT_OPEN` from Naabu/Nmap; classify IPs via `classify_ip`.
5. **`models` array** — emit child software / description nodes per model name (see nugget-mapping.md).

## Python parse sketch

```python
import json
from urllib.parse import urlparse

def iter_julius_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and line.startswith("{"):
                yield json.loads(line)

for row in iter_julius_jsonl("julius.jsonl"):
    parsed = urlparse(row["target"])
    print(parsed.hostname, parsed.port, row["service"], row.get("models"))
```
