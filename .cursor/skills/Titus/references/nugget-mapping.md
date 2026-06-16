# Titus Nugget Mapping

Convert validated findings to SpiderFeet-style `nodes` and `edges`.

## Suggested node types

- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `EMAILADDR`
- `USERNAME`

## Example payload

```json
{
  "nodes": [
    {"id": "finding:titus:abc", "type": "RAW_RIR_DATA", "label": "possible secret"},
    {"id": "email:ops@example.com", "type": "EMAILADDR", "label": "ops@example.com"}
  ],
  "edges": [
    {"from": "finding:titus:abc", "to": "email:ops@example.com", "type": "ASSOCIATED_WITH"}
  ]
}
```
