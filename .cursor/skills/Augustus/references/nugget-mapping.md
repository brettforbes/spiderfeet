# Augustus Nugget Mapping

Convert Augustus findings to SpiderFeet-style graph arrays.

## Node suggestions

- `LLM_ENDPOINT` (provider/model or REST endpoint)
- `LLM_PROBE` (probe family and exact probe name)
- `LLM_DETECTOR` (detector used for classification)
- `LLM_VULNERABILITY` (failed/suspect finding with score)
- `RAW_RIR_DATA` (optional serialized raw result blob for traceability)

## Edge suggestions

- `LLM_ENDPOINT` -> `LLM_PROBE` (`tested_with`)
- `LLM_PROBE` -> `LLM_DETECTOR` (`evaluated_by`)
- `LLM_DETECTOR` -> `LLM_VULNERABILITY` (`identified`)

## Example arrays

```json
{
  "nodes": [
    {"id":"model:openai:gpt-4","type":"LLM_ENDPOINT","data":"openai.OpenAI:gpt-4"},
    {"id":"probe:dan.Dan_11_0","type":"LLM_PROBE","data":"dan.Dan_11_0"},
    {"id":"vuln:dan:0.85","type":"LLM_VULNERABILITY","data":"DAN jailbreak score 0.85"}
  ],
  "edges": [
    {"source":"model:openai:gpt-4","target":"probe:dan.Dan_11_0","type":"tested_with"},
    {"source":"probe:dan.Dan_11_0","target":"vuln:dan:0.85","type":"identified"}
  ]
}
```
