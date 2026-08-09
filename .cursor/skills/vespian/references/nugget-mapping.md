# Vespasian Nugget Mapping

Map Vespasian **capture + generated specs** into SpiderFeet `nodes` / `edges`. Reuse catalogue ids from `.docs/analysis/nuggets.json` before inventing types. Add tool-specific ids only to `nuggets_extension.json` when the operator approves.

## Suggested nugget types

| Source | Nugget ID | Notes |
|--------|-----------|-------|
| Application / API host | `INTERNET_NAME` | From URL host / OpenAPI `servers` |
| Registered domain | `DOMAIN_NAME` | When apex is clear from host |
| Absolute same-site API URL | `LINKED_URL_INTERNAL` | Prefer full URL when known |
| Form / POST endpoints from capture | `URL_FORM` | When capture shows form submissions |
| JS-driven API URL strings | `URL_JAVASCRIPT` | When evidence is from JS bundle traffic |
| Stack / API style descriptor | `WEBSERVER_TECHNOLOGY` | e.g. `GraphQL`, `SOAP/WSDL`, `OpenAPI/REST` labels — not invented product names |
| Method + path, confidence, api_type | `RAW_RIR_DATA` | Compact descriptor until a dedicated API nugget is approved |
| Spec file identity | `RAW_RIR_DATA` | e.g. `openapi:openapi.yaml` / `graphql:schema.graphql` |

**Do not** emit non-catalogue types such as `API_ENDPOINT` or `API_PARAMETER` in formal graphs unless added to `nuggets_extension.json` and TypeQL.

## Graph pattern

```
SCAN (scan head)
  └─contains─> INTERNET_NAME (host)
        └─had─> LINKED_URL_INTERNAL | URL_FORM (endpoint URL)
        └─had─> WEBSERVER_TECHNOLOGY (API style, when justified)
        └─had─> RAW_RIR_DATA (METHOD path | confidence | api_type)
```

Allowed relations: `contains`, `had`, `listens-to` per project ontology rules. Use `core.graph_builder.nugget_instance_id` only.

## Example payload (illustrative)

```json
{
  "nodes": [
    {
      "nugget_id": "INTERNET_NAME",
      "nugget_data": "app.example.com",
      "nugget_instance_id": "INTERNET_NAME--<uuid5>"
    },
    {
      "nugget_id": "LINKED_URL_INTERNAL",
      "nugget_data": "https://app.example.com/api/v1/login",
      "nugget_instance_id": "LINKED_URL_INTERNAL--<uuid5>"
    },
    {
      "nugget_id": "RAW_RIR_DATA",
      "nugget_data": "POST /api/v1/login | api_type:rest | confidence:0.92",
      "nugget_instance_id": "RAW_RIR_DATA--<uuid5>"
    },
    {
      "nugget_id": "WEBSERVER_TECHNOLOGY",
      "nugget_data": "OpenAPI/REST",
      "nugget_instance_id": "WEBSERVER_TECHNOLOGY--<uuid5>"
    }
  ],
  "edges": [
    {"from": "<scan_instance>", "to": "<host_instance>", "relation": "contains"},
    {"from": "<host_instance>", "to": "<url_instance>", "relation": "had"},
    {"from": "<host_instance>", "to": "<desc_instance>", "relation": "had"},
    {"from": "<host_instance>", "to": "<tech_instance>", "relation": "had"}
  ]
}
```

## Validation gate

1. Endpoint URLs come from capture or generated spec — not guessed paths.
2. Every node appears in at least one edge.
3. No raw auth tokens or session cookies as `nugget_data`.
4. Clean-miss (empty paths) still produces a scan head graph.
5. Prefer OpenAPI/GraphQL/WSDL structured files over banner text for derivation.
