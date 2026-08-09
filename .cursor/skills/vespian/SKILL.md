---
name: vespian
description: Discover API endpoints from captured traffic with Vespasian and generate OpenAPI, GraphQL SDL, or WSDL. Trigger for API surface mapping, Burp/HAR/mitmproxy imports, undocumented endpoint discovery, or scan/generate pipelines.
---

# Vespasian — API Discovery and Spec Generation

## Purpose

Use when you must **map API attack surface from real HTTP traffic** on authorized targets with [Praetorian Vespasian](https://github.com/praetorian-inc/vespasian) — crawl or import captures, then generate **OpenAPI 3.x** (`rest`), **GraphQL SDL** (`graphql`), or **WSDL** (`wsdl`). Prefer structured artifacts (`capture.json` + generated specs via `-o`) for SpiderFeet graphs; chain to further API testing only within scope.

**Binary name:** `vespasian` (not `vespian`). Skill folder remains `.cursor/skills/vespian`.

| Platform | Path |
|----------|------|
| WSL | `/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian` |
| Windows path | `C:\projects\spiderfeet\.tools\vespasian\vespasian` |

**Version:** **v1.0.0** (`vespasian version` — commit `f93dab0…`, built `2026-04-03`). Help capture: **2026-08-10** (`.tmp_vespasian_help/`).

## Step-by-Step Instructions

1. **Confirm authorization** — crawling, probing, and proxying send real traffic; private/lab hosts need `--dangerous-allow-private` on `scan` / `generate` when probing.
2. **Verify binary** — `vespasian version` and `vespasian --help` (verbatim Captured help in `.docs/docs-for-cli-tools/Vespasian-CLI-Options.md`).
3. **Choose workflow**
   - **One-step:** `vespasian scan <url> -o <spec>` — crawl + classify + generate.
   - **Two-stage:** `crawl` or `import` → `capture.json`, then `generate <rest|graphql|wsdl>`.
4. **Capture traffic**
   - Live: `vespasian crawl <url> -o capture.json` (add `-H` for auth; `--headless` for browser/SPA; `--proxy` for Burp).
   - Existing: `vespasian import burp|har|mitmproxy <file> -o capture.json`.
5. **Generate structured specs** (SpiderFeet primary artifacts)
   - REST → OpenAPI: `vespasian generate rest capture.json -o openapi.yaml`
   - GraphQL → SDL: `vespasian generate graphql capture.json -o schema.graphql`
   - SOAP → WSDL: `vespasian generate wsdl capture.json -o service.wsdl`
   - Or `scan` with `--api-type auto|rest|graphql|wsdl` and `-o`.
6. **Tune coverage** — deepen crawl (`--depth`, `--max-pages`, `--timeout`); add auth headers; enable `--probe` / `--deduplicate` on generate/scan; raise `--confidence` if noisy.
7. **Parse artifacts** — read `capture.json` (observed requests) and the generated OpenAPI/GraphQL/WSDL files; see `references/output-and-parsing.md`.
8. **Map nuggets** — host → `INTERNET_NAME`; endpoint URLs → `LINKED_URL_INTERNAL` / `URL_FORM`; stack hints → `WEBSERVER_TECHNOLOGY`; method/path/confidence descriptors → `RAW_RIR_DATA` per `references/nugget-mapping.md`.
9. **Chain downstream** — feed OpenAPI/GraphQL/WSDL into authorized API testers (e.g. Hadrian) or manual review; do not treat the spec as a complete contract.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always write `-o` specs + retain `capture.json`; never parse banner/TTY alone |
| No live crawl window | `import burp\|har\|mitmproxy` then `generate` |
| SPA / heavy JavaScript | Use `--headless` (system Chrome/Chromium required for headless path) |
| Lightweight / no Chrome | Omit `--headless` (stdlib HTTP crawl per this binary’s flag surface) |
| Auth-gated APIs | Repeatable `-H "Authorization: …"` / Cookie headers on `scan`/`crawl` |
| Thin endpoint yield | Increase `--depth` / `--max-pages`; import proxy traffic; enable `--probe` |
| Noisy classification | Raise `--confidence` (default `0.5`); use `--deduplicate` before probing |
| Localhost / RFC1918 lab | `scan`/`generate` with `--dangerous-allow-private` (required for private probe targets) |
| GraphQL introspection blocked | Rely on traffic-inferred SDL from capture; keep `--probe` for tiered introspection when allowed |
| Fast triage | `scan … --api-type auto -o api.yaml` first; split to two-stage for re-generation |
| Formal examination | Prefer generated OpenAPI/GraphQL/WSDL + capture JSON as structured sources |

## Guardrails & Pitfalls

- **Authorization only** — active crawl and `--probe` hit the target; proxy MITM needs an approved intercept.
- **Do not invent flags** — authoritative surface is Captured help **2026-08-10** for **v1.0.0**. Upstream README may document `grpc`, `--analyze-js`, `--proxy-insecure`, etc.; those are **not** in this binary’s `--help` — verify before use.
- **Binary vs skill name** — invoke `vespasian`; skill id is `vespian`.
- **Discovery ≠ complete contract** — only endpoints present in captured traffic (plus probing of those candidates).
- **SSRF protection** — private/loopback probing blocked unless `--dangerous-allow-private`; never enable on production indiscriminately.
- **Headless needs Chrome** — headless path expects a system browser; failures are environment issues, not “empty API” proof.
- **Import formats** — only `burp`, `har`, `mitmproxy` (help). Nested help stubs for other names still list those three.
- **Generate API types** — only `rest`, `graphql`, `wsdl` on this binary (not `grpc` in Captured help).
- **TLS note** — help states certificate verification is disabled during crawls when using `--proxy` for the headless browser path.
- **Preserve captures** — `capture.json` is the evidence source; regenerate specs without re-crawling when possible.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, SpiderFeet defaults, Captured help pointer |
| `output-and-parsing.md` | `capture.json`, OpenAPI / GraphQL / WSDL |
| `nugget-mapping.md` | Specs → SpiderFeet `nodes[]` / `edges[]` |
| `tactics.md` | Sequencing, thin yield, proxy/import tactics |
| `sources.md` | Official repo, blog, releases |

Operator guides: `.docs/docs-for-cli-tools/Vespasian-Zero-to-Hero.md`, `Vespasian-CLI-Options.md`.

## Comprehensive Examples

### ONE-STEP SCAN

```bash
vespasian scan https://app.example.com -o api.yaml
vespasian scan https://app.example.com --api-type graphql -o schema.graphql
vespasian scan https://app.example.com -H "Authorization: Bearer <token>" -o api.yaml
vespasian --no-banner scan https://app.example.com -o api.yaml
```

### TWO-STAGE (CRAWL → GENERATE)

```bash
vespasian crawl https://app.example.com -o capture.json
vespasian generate rest capture.json -o openapi.yaml
vespasian generate graphql capture.json -o schema.graphql
vespasian generate wsdl capture.json -o service.wsdl
```

### IMPORT PROXY TRAFFIC

```bash
vespasian import burp traffic.xml -o capture.json
vespasian import har recording.har -o capture.json
vespasian import mitmproxy flows -o capture.json
vespasian generate rest capture.json -o openapi.yaml
```

### CRAWL TUNING / PROXY

```bash
vespasian crawl https://app.example.com --depth 5 --max-pages 200 --timeout 15m -o capture.json
vespasian crawl https://app.example.com --headless --proxy http://127.0.0.1:8080 -o capture.json
vespasian scan https://app.example.com --proxy http://127.0.0.1:8080 -o api.yaml
```

### PROBE / CONFIDENCE / PRIVATE LAB

```bash
vespasian generate rest capture.json --probe --deduplicate --confidence 0.7 -o openapi.yaml
vespasian scan http://localhost:3000 --dangerous-allow-private -o api.yaml
vespasian generate rest capture.json --dangerous-allow-private --probe -o openapi.yaml
```

### PREFERRED SPIDERFEET PATH (WSL)

```bash
/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian \
  scan https://app.example.com -o openapi.yaml
```

### PARSE OPENAPI PATHS (Python sketch)

```python
import yaml  # or json if the file is JSON OpenAPI

with open("openapi.yaml", encoding="utf-8") as f:
    spec = yaml.safe_load(f)
paths = spec.get("paths") or {}
for path, methods in paths.items():
    for method in methods:
        if method.startswith("x-") or method in ("parameters", "summary", "description"):
            continue
        # → LINKED_URL_INTERNAL / RAW_RIR_DATA("METHOD path")
        print(method.upper(), path)
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Scan first for triage** — `scan --api-type auto -o …`, then two-stage for repeatable capture/spec diffs.
2. **Capture once, generate many** — keep `capture.json`; re-run `generate rest|graphql|wsdl` without re-crawling.
3. **Combine crawl + import** — browser crawl for SPA XHR; Burp/HAR/mitmproxy for authenticated or mobile flows.
4. **Auth before depth** — headers often beat larger `--max-pages` on gated APIs.
5. **Structured-first** — OpenAPI/GraphQL/WSDL + capture JSON are the examination sources; map URLs/hosts to catalogue nuggets.
