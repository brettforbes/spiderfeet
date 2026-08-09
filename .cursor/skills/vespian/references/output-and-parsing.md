# Vespasian Output and Parsing

Vespasian separates **capture** from **specification generation**. SpiderFeet examination should treat those files as the structured sources (not TTY banners).

## Primary artifacts

| Artifact | Produced by | Role |
|----------|-------------|------|
| `capture.json` | `crawl -o`, `import … -o` | Observed HTTP requests (inspectable JSON) |
| OpenAPI 3.x | `generate rest`, `scan` (REST/`auto`→REST) | Paths, methods, parameters, schemas |
| GraphQL SDL | `generate graphql`, `scan --api-type graphql` | Types / operations from introspection or traffic |
| WSDL XML | `generate wsdl`, `scan --api-type wsdl` | SOAP service contract |

Default without `-o` is typically stdout (per upstream docs); always pass `-o` for corpus bundles.

## Capture JSON

- Array (or documented container) of observed requests from crawl/import.
- Upstream notes multi-value query params as `map[string][]string` — regenerate old captures if field shape drifts.
- Preserve the capture as evidence even when regenerating specs.

## Generated specs

### REST → OpenAPI

Parse YAML or JSON OpenAPI:

- `paths` → endpoint map
- Per-method `parameters`, `requestBody`, `responses`
- `servers` / host for `INTERNET_NAME` correlation

### GraphQL → SDL

Parse `.graphql` / SDL text for `type`, `query`, `mutation`, `subscription` definitions. When introspection fails, SDL may be partial and traffic-inferred.

### WSDL → XML

Parse WSDL for `service`, `port`, `binding`, `operation`, and message parts. Correlate SOAPAction / `?wsdl` origins from the capture when present.

## Parsing priorities

1. Keep `capture.json` as the evidence spine (what was actually observed).
2. Parse the generated spec for normalized operations.
3. Correlate spec operations back to capture URLs/methods.
4. Record confidence / probe enrichment only when present in tool output or operator notes — do not invent fields absent from artifacts.

## Suggested normalized endpoint record (harvest intermediate)

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

Build this from OpenAPI/GraphQL/WSDL + capture; do not invent a Vespasian JSONL mode that the binary does not expose.

## Harvest / SpiderFeet notes

- Prefer a **JSON bundle** for the Structured pane: scan metadata + `records[]` of normalized endpoints, plus paths to the native OpenAPI/GraphQL/WSDL files.
- Derive Text pane lines from those records (e.g. `POST https://host/path`).
- Empty `paths` / empty capture with successful exit can be a valid clean-miss scenario — still emit graph head + sparse tree.
- Never treat the startup banner as findings.

## Guardrails

- Deduplicate normalized dynamic paths (`/users/42` → `/users/{id}`) when the generator already parameterized them.
- Flag low-confidence or unresolved items; do not silently drop without recording sparse coverage.
- Auth headers used during crawl are sensitive — store captures access-controlled.
