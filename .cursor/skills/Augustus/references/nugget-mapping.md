# Augustus Nugget Mapping

Map Augustus **structured attempts** into SpiderFeet `nodes` / `edges`. Reuse catalogue ids from `.docs/analysis/nuggets.json` before inventing types. Add tool-specific ids only to `nuggets_extension.json` when the operator approves.

## Suggested nugget types

| Source | Nugget ID | Notes |
|--------|-----------|-------|
| Target host / API host (from `rest.Rest` URI) | `INTERNET_NAME` | Hostname only when known |
| Model / provider label | `WEBSERVER_TECHNOLOGY` or `RAW_RIR_DATA` | e.g. `openai.OpenAI:gpt-4` as descriptor until a dedicated LLM type exists |
| Confirmed / scored vulnerability attempt | `VULNERABILITY_GENERAL` | Prefer when detector indicates vuln / high score — do not invent severity tiers |
| Probe name, detector name, score, status, harness, buff | `RAW_RIR_DATA` | Compact descriptors: `probe:dan.Dan_11_0`, `detector:dan.DAN`, `score:0.85` |
| Scan identity | scan head via shared topology | Tool + command + timestamp |

**Do not** emit non-catalogue types such as `LLM_ENDPOINT`, `LLM_PROBE`, or `LLM_VULNERABILITY` in formal graphs unless added to `nuggets_extension.json` and TypeQL.

## Graph pattern

```
SCAN (scan head)
  └─contains─> INTERNET_NAME (API host, when known)
        └─had─> WEBSERVER_TECHNOLOGY | RAW_RIR_DATA (generator/model)
        └─had─> VULNERABILITY_GENERAL (finding summary, when justified)
        └─had─> RAW_RIR_DATA (probe | detector | score | status)
```

When there is no HTTP host (e.g. `openai.OpenAI` cloud API), attach descriptors under the scan head (or a synthetic system label via `RAW_RIR_DATA`) — do not invent hostnames.

Allowed relations: `contains`, `had`, `listens-to` per project ontology rules. Use `core.graph_builder.nugget_instance_id` only.

## Example payload (illustrative)

```json
{
  "nodes": [
    {
      "nugget_id": "INTERNET_NAME",
      "nugget_data": "api.example.com",
      "nugget_instance_id": "INTERNET_NAME--<uuid5>"
    },
    {
      "nugget_id": "VULNERABILITY_GENERAL",
      "nugget_data": "dan.Dan_11_0 / dan.DAN score=0.85",
      "nugget_instance_id": "VULNERABILITY_GENERAL--<uuid5>"
    },
    {
      "nugget_id": "RAW_RIR_DATA",
      "nugget_data": "generator:rest.Rest | probe:dan.Dan_11_0 | detector:dan.DAN | status:complete",
      "nugget_instance_id": "RAW_RIR_DATA--<uuid5>"
    }
  ],
  "edges": [
    {"from": "<scan_instance>", "to": "<host_instance>", "relation": "contains"},
    {"from": "<host_instance>", "to": "<vuln_instance>", "relation": "had"},
    {"from": "<host_instance>", "to": "<desc_instance>", "relation": "had"}
  ]
}
```

## Validation gate

1. Findings come from structured JSON/JSONL — not table text.
2. Every node appears in at least one edge.
3. No raw API keys or full jailbreak prompts as `nugget_data` in shared graphs (summarize).
4. Clean-miss (all SAFE / empty attempts) still produces a scan head graph.
5. Prefer catalogue `VULNERABILITY_GENERAL` + descriptors over invented LLM-specific types.
