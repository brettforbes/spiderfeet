# Katana Nugget Mapping

## Typical Inputs

- `INTERNET_NAME`
- `URL`

## Typical Outputs

- `URL` (discovered endpoints/assets)
- `INTERNET_NAME` (derived hosts/subdomains)
- optional raw metadata nuggets as needed

## Node/Edge Mapping

- Create URL node per canonical URL.
- Create host node per hostname.
- Edge host -> URL as `DISCOVERED_URL`.

## nodes/edges Example

```json
{
  "nodes": [
    {"id": "host:example.org", "type": "INTERNET_NAME", "data": {"value": "example.org"}},
    {"id": "url:https://example.org/login", "type": "URL", "data": {"value": "https://example.org/login"}}
  ],
  "edges": [
    {"source": "host:example.org", "target": "url:https://example.org/login", "type": "DISCOVERED_URL"}
  ]
}
```
