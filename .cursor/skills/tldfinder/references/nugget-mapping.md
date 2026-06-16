# tldfinder -> SpiderFeet Nugget Mapping

Map discovered private/rare namespace findings into graph payloads with `nodes[]` and `edges[]`.

## Node mapping

| Finding | Node type |
|---|---|
| Seed domain/host | `INTERNET_NAME` |
| Candidate private TLD namespace | `INTERNET_NAME` (suffix marker in metadata) |
| Expanded candidate host | `INTERNET_NAME` |

## Edge mapping

| Relationship | Edge |
|---|---|
| Seed implies namespace candidate | `INTERNET_NAME` -> `INTERNET_NAME` (`suggests_private_tld`) |
| Namespace expands to host candidate | `INTERNET_NAME` -> `INTERNET_NAME` (`expands_to_candidate_host`) |

## Example graph payload

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "corp.example.com" },
    { "type": "INTERNET_NAME", "data": ".corp", "meta": { "namespace_candidate": true } },
    { "type": "INTERNET_NAME", "data": "vpn.gateway.corp" }
  ],
  "edges": [
    { "source": "corp.example.com", "target": ".corp", "relationship": "suggests_private_tld" },
    { "source": ".corp", "target": "vpn.gateway.corp", "relationship": "expands_to_candidate_host" }
  ]
}
```

## Confidence metadata guidance

- Store confidence score and evidence count in edge metadata.
- Promote only high-confidence namespaces into active validation pipelines.
