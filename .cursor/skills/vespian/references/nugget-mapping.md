# Vespasian Nugget Mapping

Map Vespasian discovery output into SpiderFeet-style `nodes` and `edges`.

## Node suggestions

- `INTERNET_NAME` (application host)
- `API_ENDPOINT` (normalized path + method)
- `API_PARAMETER` (query/path/body parameter)
- `API_SPEC_ARTIFACT` (OpenAPI, GraphQL SDL, or WSDL file)
- `WEBSERVER_TECHNOLOGY` (if observed from response metadata/captured headers)

## Edge suggestions

- `INTERNET_NAME` -> `API_ENDPOINT` (`exposes`)
- `API_ENDPOINT` -> `API_PARAMETER` (`uses_parameter`)
- `API_ENDPOINT` -> `API_SPEC_ARTIFACT` (`documented_in`)

## Example arrays

```json
{
  "nodes": [
    {"id":"host:app.example.com","type":"INTERNET_NAME","data":"app.example.com"},
    {"id":"ep:POST:/api/v1/login","type":"API_ENDPOINT","data":"POST /api/v1/login"},
    {"id":"param:email","type":"API_PARAMETER","data":"email"}
  ],
  "edges": [
    {"source":"host:app.example.com","target":"ep:POST:/api/v1/login","type":"exposes"},
    {"source":"ep:POST:/api/v1/login","target":"param:email","type":"uses_parameter"}
  ]
}
```
