# dnsx -> SpiderFeet Nugget Mapping

This mapping converts dnsx findings into graph payloads with explicit `nodes[]` and `edges[]` arrays.

## Node conversion

| dnsx signal | Node type | `data` suggestion |
|---|---|---|
| Queried host/subdomain | `INTERNET_NAME` | fqdn |
| A/AAAA answer IP | `IP_ADDRESS` | ip |
| CNAME target | `INTERNET_NAME` | canonical hostname |
| MX server | `INTERNET_NAME` | mail exchanger host |
| NS server | `INTERNET_NAME` | authoritative nameserver |
| TXT policy string | `RAW_RIR_DATA` or module-specific text node | txt payload |

## Edge conversion

| Relationship | Edge shape |
|---|---|
| host resolves to IP | `INTERNET_NAME` -> `IP_ADDRESS` |
| host aliases to CNAME | `INTERNET_NAME` -> `INTERNET_NAME` |
| domain uses MX | `INTERNET_NAME` -> `INTERNET_NAME` |
| domain delegated to NS | `INTERNET_NAME` -> `INTERNET_NAME` |

## Example output contract

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "api.example.com" },
    { "type": "IP_ADDRESS", "data": "203.0.113.20" },
    { "type": "INTERNET_NAME", "data": "dualstack.edge.example.net" }
  ],
  "edges": [
    { "source": "api.example.com", "target": "203.0.113.20", "relationship": "resolves_to" },
    { "source": "api.example.com", "target": "dualstack.edge.example.net", "relationship": "cname_to" }
  ]
}
```

## Deduplication guidance

- Node identity key: `type + normalized data`.
- Edge identity key: `source + target + relationship`.
- Keep first-seen evidence reference and append additional raw responses as metadata history.
