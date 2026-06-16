# Vespasian Output and Parsing

Vespasian separates discovery into capture and generation artifacts.

## Primary artifacts

- `capture.json` - observed request collection from crawl/import.
- generated spec:
  - OpenAPI 3.x (`rest`)
  - GraphQL SDL (`graphql`)
  - WSDL XML (`wsdl`)

## Parsing priorities

1. Parse capture records first to preserve evidence of observed behavior.
2. Parse generated spec to structure endpoints/operations.
3. Correlate endpoint paths back to source requests.
4. Keep API type confidence and probing-derived enrichment metadata.

## Suggested normalized endpoint record

```json
{
  "api_type": "rest",
  "method": "POST",
  "path": "/api/v1/login",
  "host": "app.example.com",
  "source": "capture+generate",
  "confidence": 0.92
}
```

## Parser guardrails

- Handle multi-value query parameters.
- Deduplicate normalized dynamic paths (`/users/42` -> `/users/{id}`).
- Keep unresolved or low-confidence items flagged, not silently dropped.
- Preserve imports/crawls metadata to explain coverage boundaries.
