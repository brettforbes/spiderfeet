# NTLMRecon Nugget Mapping

Convert parsed challenge metadata into SpiderFeet-style `nodes` and `edges`.

## Suggested node types

- `IP_ADDRESS`
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `OPERATING_SYSTEM` (only with strong confidence)
- `RAW_RIR_DATA`

## Example payload

```json
{
  "nodes": [
    {"id": "ip:10.10.10.20", "type": "IP_ADDRESS", "label": "10.10.10.20"},
    {"id": "host:dc01.corp.local", "type": "INTERNET_NAME", "label": "dc01.corp.local"}
  ],
  "edges": [
    {"from": "ip:10.10.10.20", "to": "host:dc01.corp.local", "type": "RESOLVES_TO"}
  ]
}
```
