# Vespasian Tactics and Workflows

## Workflow A — Fast recon (`scan`)

1. Confirm live target (optional: **httpx** first).
2. `vespasian scan https://app.example.com -o api.yaml` (`--api-type auto`).
3. Review endpoint count / OpenAPI paths.
4. Re-run with `-H` auth and higher `--depth` / `--max-pages` if thin.
5. Enable `--probe` / `--deduplicate` when classification looks incomplete.

## Workflow B — Repeatable pipeline (`crawl` → `generate`)

1. `vespasian crawl <url> -o capture.json` (or `import`).
2. Version the capture for the engagement.
3. `vespasian generate rest|graphql|wsdl capture.json -o <spec>` as needed — capture once, generate many.
4. Diff specs across confidence/probe settings without re-crawling.

## Workflow C — Proxy-assisted / authenticated

1. Route with `--proxy http://127.0.0.1:8080` and/or drive the app manually in Burp.
2. Export Burp XML / HAR / mitmproxy dump.
3. `vespasian import burp|har|mitmproxy <file> -o capture.json`.
4. `generate` with `--probe` when the origin is still reachable and probing is authorized.

## Workflow D — Private lab

1. Use `scan` or `generate` with `--dangerous-allow-private` for localhost/RFC1918.
2. Keep the flag off for internet-facing production assessments.
3. Note: Captured **crawl** help for v1.0.0 does not list `--dangerous-allow-private`; prefer `scan` for private one-step runs, or verify crawl behavior before relying on private crawl-only.

## Tactics

| Situation | Action |
|-----------|--------|
| SPA / XHR-heavy | `--headless` + system Chrome; import Burp for logged-in journeys |
| Thin yield | Auth headers first; then depth/pages; then import proxy traffic |
| Noisy REST classification | Raise `--confidence`; keep `--deduplicate` with `--probe` |
| GraphQL behind WAF | Keep `--probe` for tiered introspection; fall back to traffic-inferred SDL |
| SOAP | `generate wsdl` / `--api-type wsdl`; look for SOAPAction / `?wsdl` in capture |
| Need structured corpus | Always `-o` OpenAPI/GraphQL/WSDL + keep `capture.json` |
| Downstream testing | Feed OpenAPI into authorized API scanners (e.g. Hadrian) within scope |

## Pipeline sketches

```bash
# Live confirm → API map
httpx -u https://app.example.com -silent
vespasian scan https://app.example.com -H "Authorization: Bearer $TOKEN" -o openapi.yaml

# Manual Burp session → OpenAPI
vespasian import burp engagement.xml -o capture.json
vespasian generate rest capture.json --probe --deduplicate -o openapi.yaml
```

## Thin-yield checklist

1. Auth headers present?
2. Headless Chrome available when SPA?
3. Proxy import of real user flows?
4. `--probe` enabled on generate/scan?
5. `--confidence` not set too high?
6. Scope still `same-origin` — expand only if documented by verified scope values for your build?
