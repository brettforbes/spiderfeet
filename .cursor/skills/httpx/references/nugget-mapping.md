# httpx JSONL → SpiderFeet Nugget Mapping

Convert **`-json`** JSON Lines into graph payloads with `nodes[]` and `edges[]`. Catalogue ids from `.docs/analysis/nuggets.json`.

## Primary mappings

| httpx field | nugget_id | `data` / notes |
|-------------|-----------|----------------|
| `url` (final) | `LINKED_URL_INTERNAL` | Full URL string |
| `host` / URL host | `INTERNET_NAME` | FQDN without path |
| `ip` | `IP_ADDRESS` | When `-ip` present |
| `status_code` | `HTTP_CODE` | Numeric code as string |
| `webserver` | `WEBSERVER_BANNER` | Server banner |
| `header` / headers map | `WEBSERVER_HTTPHEADERS` | Serialized headers when captured |
| each `tech[]` entry | `WEBSERVER_TECHNOLOGY` | One node per technology |
| `cdn_name` / CDN metadata | `PROVIDER_HOSTING` or metadata | When policy matches catalogue |
| body / `body_preview` | `TARGET_WEB_CONTENT` | Only when body capture in scope |
| `title` | metadata on URL node | `title` field on node meta |

Aligns with unified ontology **APPLICATIONS** / web layer on qualified `HOST` (see `_Current_Ontology.md`).

## Example: rich probe row

Input:

```json
{
  "url": "https://api.example.com/v1",
  "status_code": 200,
  "webserver": "nginx/1.18.0",
  "tech": ["Nginx", "PHP"],
  "ip": "203.0.113.10",
  "title": "API Gateway"
}
```

Output contract:

```json
{
  "nodes": [
    {"type": "LINKED_URL_INTERNAL", "data": "https://api.example.com/v1", "meta": {"title": "API Gateway", "status_code": 200}},
    {"type": "INTERNET_NAME", "data": "api.example.com"},
    {"type": "IP_ADDRESS", "data": "203.0.113.10"},
    {"type": "HTTP_CODE", "data": "200"},
    {"type": "WEBSERVER_BANNER", "data": "nginx/1.18.0"},
    {"type": "WEBSERVER_TECHNOLOGY", "data": "Nginx"},
    {"type": "WEBSERVER_TECHNOLOGY", "data": "PHP"}
  ],
  "edges": [
    {"source": "api.example.com", "target": "203.0.113.10", "relationship": "resolves_to"},
    {"source": "https://api.example.com/v1", "target": "api.example.com", "relationship": "hosted_on"},
    {"source": "https://api.example.com/v1", "target": "200", "relationship": "had"},
    {"source": "https://api.example.com/v1", "target": "nginx/1.18.0", "relationship": "had"},
    {"source": "https://api.example.com/v1", "target": "Nginx", "relationship": "uses_technology"}
  ]
}
```

## Redirect chain

When `chain[]` present, emit each hop URL as `LINKED_URL_INTERNAL` with `redirects_to` edges toward final `url`.

## Deduplication

- URL node key: normalized URL (scheme + host + path policy).
- Tech node key: `WEBSERVER_TECHNOLOGY` + canonical tech name.
- Merge duplicate probes from HTTP/HTTPS fallback unless scenario keeps both.

## Provenance (corpus / Tests tab)

- `source_tool`: `httpx`
- `source_command`: full CLI
- `source_artifact`: path to JSONL or bundle JSON
- `probe_profile`: flags used (`tech-detect`, `include-chain`, etc.)

## Downstream

| Tool | Input |
|------|--------|
| nuclei | `url` values from JSONL |
| webanalyze | URLs or hosts for alternate fingerprint |
| Julius | HTTP URLs on AI-related ports |

## Do not emit

- `HTTP_CODE` without URL/host context
- Duplicate `WEBSERVER_TECHNOLOGY` for same URL+tech pair
- Full response body as nugget when scenario did not authorize storage

## Instance identity

`nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"` per `graph_builder.py`.
