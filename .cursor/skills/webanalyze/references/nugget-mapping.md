# webanalyze → SpiderFeet Nugget Mapping

Convert **`-output json`** host objects into graph payloads with `nodes[]` and `edges[]`. Resolve colours/icons from `.docs/analysis/nuggets.json` / `nuggets_extension.json` — do not hard-code.

## Primary mappings

| Source field | nugget_id | `nugget_data` / notes |
|--------------|-----------|------------------------|
| `hostname` host part | `INTERNET_NAME` | FQDN only (no scheme/path) |
| `hostname` full URL (optional) | `LINKED_URL_INTERNAL` | When pipeline keeps URL entities |
| each `matches[].app_name` | `WEBSERVER_TECHNOLOGY` | Append `version` when non-empty: `"Hugo 0.42.1"` |
| `app.category_names` | metadata | Store on technology node/edge meta; not a separate nugget id unless catalogue adds one |
| full host JSON line | provenance / `RAW_RIR_DATA` (optional) | Only if a module needs full raw preserve — prefer structured bundle path |

## Edge mapping (allowed relations)

Prefer shared ontology relations (`contains`, `had`, `listens-to`):

| From | Relation | To |
|------|----------|-----|
| Scan / host stack | `contains` | `INTERNET_NAME` |
| `INTERNET_NAME` | `had` | each `WEBSERVER_TECHNOLOGY` |
| `LINKED_URL_INTERNAL` (if used) | `had` | each `WEBSERVER_TECHNOLOGY` |

## Example conversion

Input line:

```json
{
  "hostname": "https://shop.example.com",
  "matches": [
    { "app_name": "Nginx", "version": "", "app": { "category_names": ["Web servers"] } },
    { "app_name": "WordPress", "version": "6.4.2", "app": { "category_names": ["CMS", "Blogs"] } }
  ]
}
```

Graph contract:

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "shop.example.com" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "Nginx" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "WordPress 6.4.2" }
  ],
  "edges": [
    { "source": "shop.example.com", "target": "Nginx", "relationship": "had" },
    { "source": "shop.example.com", "target": "WordPress 6.4.2", "relationship": "had" }
  ]
}
```

Use `core.graph_builder` instance ids (`nugget_id--uuid5(...)`) in real adapters — example above is logical only.

## Deduplication and quality

- Node identity: `(WEBSERVER_TECHNOLOGY, canonical name[+version])`.
- Keep `category_names`, evidence `matches`, and `app.website` in metadata, not in the identity key unless version is part of the chosen data string.
- Empty `matches: []` is a valid clean-miss structured record (scan head + host, no tech nodes).
- Do not invent confidence scores — webanalyze JSON does not emit a confidence field.

## Downstream pivots

| Detection signal | Next skill / tool |
|------------------|-------------------|
| CMS / blog categories | CMSeeK, Nuclei CMS tags |
| CDN / security categories | wafw00f |
| Web server / language / framework | httpx confirm, Nuclei tech tags |
