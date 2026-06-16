---
name: vespian
description: Discover API endpoints from captured traffic with Vespasian and generate OpenAPI, GraphQL SDL, or WSDL. Trigger for API surface mapping, Burp/HAR/mitmproxy imports, undocumented endpoint discovery, or scan/generate pipelines.
---

# Vespasian - API Discovery and Spec Generation

## Purpose

Use this skill to discover API attack surface from real HTTP traffic, generate machine-readable API specifications, and convert endpoint intelligence into SpiderFeet-style nugget graphs.

## Step-by-Step Instructions

1. Confirm authorized target and choose workflow: one-step `scan` or two-stage `crawl/import` + `generate`.
2. Capture traffic:
   - `scan`/`crawl` for live target crawling.
   - `import burp|har|mitmproxy` for existing captures.
3. Classify output target type: `rest`, `graphql`, or `wsdl` (or `auto` in `scan`).
4. Generate spec and retain raw capture JSON for traceability.
5. Parse discovered endpoints and operations.
6. Convert parsed assets into SpiderFeet-style nuggets:
   - `nodes`: application, endpoint path, method, parameter, API type.
   - `edges`: application exposes endpoint, endpoint uses parameter, endpoint belongs-to API type.
7. Re-run with adjusted depth/confidence/probe settings when coverage is insufficient.

## If/Then Decision Rules

- If you have no live access window, then use `import` from Burp/HAR/mitmproxy.
- If JavaScript-heavy SPA behavior is needed, then keep `--headless=true`.
- If target is private/local lab host, then explicitly set `--dangerous-allow-private`.
- If generation is noisy, then raise `--confidence` and enable deduplication.
- If GraphQL introspection fails, then rely on traffic-based inference from captured operations.
- If fast triage is needed, then run `scan` first and split into two-stage workflow only for deep validation.

## Guardrails & Pitfalls

- Authorized testing only.
- Discovery is bounded by observed traffic; unvisited flows remain undiscovered.
- Do not disable SSRF protections outside controlled lab contexts.
- Preserve capture files; they are your evidence source.
- Treat generated specs as discovered surface, not guaranteed full contract.

## Strategies and Tactics

- Use one-step `scan` for rapid recon, then two-stage for repeatable engineering workflows.
- Combine dynamic crawl with imported proxy traffic for broader endpoint coverage.
- Prioritize auth, admin, and mutation endpoints for downstream testing.
- Feed generated specs into further security tooling.

## References

See `references/SKILLS.md` for full CLI, parsing schema, nugget mapping, tactics/workflows, and sources.

## Examples

```bash
# One-step scan with auto API type
vespasian scan https://app.example.com -o api.yaml

# Crawl then generate REST OpenAPI
vespasian crawl https://app.example.com -o capture.json
vespasian generate rest capture.json -o openapi.yaml

# Import Burp XML then generate GraphQL SDL
vespasian import burp traffic.xml -o capture.json
vespasian generate graphql capture.json -o schema.graphql

# Scan private target in lab
vespasian scan http://localhost:3000 --dangerous-allow-private -o api.yaml
```
