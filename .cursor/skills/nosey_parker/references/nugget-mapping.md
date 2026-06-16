# nosey_parker Nugget Mapping

Convert validated findings into SpiderFeet-style `nodes` and `edges` arrays.

## Suggested node types

- `RAW_RIR_DATA`
- `INTERNET_NAME`
- `EMAILADDR`
- `USERNAME`

## Example payload

```json
{
  "nodes": [
    {"id": "finding:np:abc", "type": "RAW_RIR_DATA", "label": "possible secret finding"},
    {"id": "domain:api.example.com", "type": "INTERNET_NAME", "label": "api.example.com"}
  ],
  "edges": [
    {"from": "finding:np:abc", "to": "domain:api.example.com", "type": "RELATED_TO"}
  ]
}
```
