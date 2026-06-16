# webanalyze -> SpiderFeet Nugget Mapping

Convert webanalyze technology detections to explicit `nodes[]` and `edges[]` graph payloads.

## Node mapping

| Detection | Node type |
|---|---|
| Scanned host/domain | `INTERNET_NAME` |
| Detected product/framework/server | `WEBSERVER_TECHNOLOGY` |
| Optional URL-level context | `LINKED_URL_INTERNAL` or `URL`-class node if pipeline uses URL entities |

## Edge mapping

| Relation | Edge |
|---|---|
| Host uses technology | `INTERNET_NAME` -> `WEBSERVER_TECHNOLOGY` (`uses_technology`) |
| URL reveals technology | `URL_NODE` -> `WEBSERVER_TECHNOLOGY` (`fingerprinted_as`) |

## Example conversion

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "shop.example.com" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "Nginx" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "Vue.js" }
  ],
  "edges": [
    { "source": "shop.example.com", "target": "Nginx", "relationship": "uses_technology" },
    { "source": "shop.example.com", "target": "Vue.js", "relationship": "uses_technology" }
  ]
}
```

## Deduplication and quality

- Normalize technology names (case, aliases) before dedupe.
- Keep category/version/confidence in metadata, not in node identity key.
- Preserve first evidence and append later confirmations as metadata history.
