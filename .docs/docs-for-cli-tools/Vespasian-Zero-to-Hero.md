# Vespasian Zero to Hero — API Discovery from Real Traffic

Operator guide from install through crawl/import, OpenAPI / GraphQL / WSDL generation, and SpiderFeet nugget mapping.

Skill reference: `.cursor/skills/vespian/SKILL.md`

**Binary name:** `vespasian` (Praetorian). Skill folder: `vespian`.

---

## 0. What Vespasian does

**Vespasian** ([praetorian-inc/vespasian](https://github.com/praetorian-inc/vespasian)) discovers API endpoints by **observing real HTTP traffic**, then generates machine-readable specs:

| API style | Generator arg | Output |
|-----------|---------------|--------|
| REST | `rest` | OpenAPI 3.x |
| GraphQL | `graphql` | GraphQL SDL |
| SOAP | `wsdl` | WSDL XML |

Traffic comes from a **crawl** (optional headless browser) or **import** of Burp XML, HAR, or mitmproxy dumps. The one-step `scan` command crawls, classifies, and generates in a single run.

Vespasian does **not**:

- Replace passive subdomain enumeration (**subfinder**)
- Replace HTTP live probing (**httpx**)
- Run vulnerability templates (**nuclei**)

**SpiderFeet uses:** `-o` capture JSON + generated OpenAPI/GraphQL/WSDL → hosts/URLs → `INTERNET_NAME` / `LINKED_URL_INTERNAL` / related nuggets.

**This guide matches binary v1.0.0** (Captured help **2026-08-10**). Do not invent flags from newer README sections until they appear in `--help` for your build.

---

## 1. Install

### Local SpiderFeet binary (authoritative on this host)

```bash
# WSL
/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian version

# Windows path to the same file
# C:\projects\spiderfeet\.tools\vespasian\vespasian
```

### Go install

```bash
go install github.com/praetorian-inc/vespasian/cmd/vespasian@latest
vespasian version
```

### Prebuilt release

Download from [GitHub releases](https://github.com/praetorian-inc/vespasian/releases), extract, `chmod +x`, run `vespasian version`.

### Verify

```bash
wsl bash -lc "/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian --help"
```

Captured help: `.docs/docs-for-cli-tools/Vespasian-CLI-Options.md` (date **2026-08-10**).

---

## 2. First scan (one-step)

```bash
vespasian scan https://app.example.com -o api.yaml
```

This crawls the target, classifies API traffic, and writes a spec (`--api-type` defaults to `auto`).

With authentication:

```bash
vespasian scan https://app.example.com \
  -H "Authorization: Bearer <token>" \
  -o api.yaml
```

Force GraphQL SDL:

```bash
vespasian scan https://app.example.com --api-type graphql -o schema.graphql
```

Suppress banner:

```bash
vespasian --no-banner scan https://app.example.com -o api.yaml
```

---

## 3. Two-stage workflow (recommended for corpus)

### Stage 1 — Capture

```bash
vespasian crawl https://app.example.com -o capture.json
```

Or import existing traffic:

```bash
vespasian import burp traffic.xml -o capture.json
vespasian import har recording.har -o capture.json
vespasian import mitmproxy flows -o capture.json
```

### Stage 2 — Generate specs

```bash
vespasian generate rest capture.json -o openapi.yaml
vespasian generate graphql capture.json -o schema.graphql
vespasian generate wsdl capture.json -o service.wsdl
```

**Why two stages:** capture once, regenerate many times; inspect `capture.json` when classification looks wrong; re-run generate offline when the engagement window closed (probing still needs reachability when `--probe` is used).

---

## 4. Essential flags (v1.0.0 Captured help)

| Flag | Where | Purpose |
|------|-------|---------|
| `-o, --output` | all writers | **Always set** for SpiderFeet artifacts |
| `-H, --header` | crawl / scan | Auth and custom headers (repeatable) |
| `--depth` / `--max-pages` / `--timeout` | crawl / scan | Crawl budget (defaults `3` / `100` / `10m`) |
| `--scope` | crawl / scan | Default `same-origin` |
| `--headless` | crawl / scan | Use headless browser (needs system Chrome/Chromium for that path) |
| `--proxy` | crawl / scan | e.g. `http://127.0.0.1:8080` (help: TLS verification disabled during crawls) |
| `--confidence` | generate / scan | Min classification confidence (default `0.5`) |
| `--probe` | generate / scan | Active endpoint probing |
| `--deduplicate` | generate / scan | Deduplicate before probing |
| `--dangerous-allow-private` | generate / scan | Allow private/localhost probes (lab only) |
| `--api-type` | scan | `auto` (default) or force type |
| `--no-request-id` | crawl / scan | Disable `X-Vespasian-Request-Id` |
| `-v, --verbose` | most | Verbose logging |
| `--no-banner` | global | Suppress banner |

Full verbatim help: `Vespasian-CLI-Options.md`.

---

## 5. Expand coverage

1. Add auth with `-H` before blindly raising crawl size.
2. Use `--headless` for SPA/XHR-heavy apps (Chrome available).
3. Import Burp/HAR sessions for logged-in or mobile flows.
4. Enable `--probe` and `--deduplicate` on generate/scan.
5. Raise `--depth` / `--max-pages` / `--timeout` when the app is deep.
6. Tune `--confidence` if the OpenAPI is noisy or sparse.

---

## 6. Private / lab targets

```bash
vespasian scan http://localhost:3000 --dangerous-allow-private -o api.yaml
```

Help warns: do **not** use `--dangerous-allow-private` on production systems. Captured **crawl** help for v1.0.0 does not list this flag — prefer `scan` (or `generate` with probe) for private labs unless you verify crawl behavior separately.

---

## 7. Structured artifacts for SpiderFeet

Prefer these over TTY text:

1. **`capture.json`** — observed requests (evidence).
2. **OpenAPI / GraphQL SDL / WSDL** — normalized operations.

There is no separate `--json` findings mode on v1.0.0; the specs and capture files *are* the structured outputs.

Parse OpenAPI `paths` into endpoint records, then map:

| Value | Nugget (catalogue) |
|-------|---------------------|
| Host | `INTERNET_NAME` |
| Endpoint URL | `LINKED_URL_INTERNAL` / `URL_FORM` |
| API style label | `WEBSERVER_TECHNOLOGY` |
| `METHOD path` + confidence | `RAW_RIR_DATA` |

Details: `.cursor/skills/vespian/references/nugget-mapping.md`.

---

## 8. Pipelines

```bash
# Confirm live → map APIs
httpx -u https://app.example.com -silent
vespasian scan https://app.example.com -H "Authorization: Bearer $TOKEN" -o openapi.yaml

# Manual Burp work → OpenAPI
vespasian import burp engagement.xml -o capture.json
vespasian generate rest capture.json --probe --deduplicate -o openapi.yaml
```

Downstream: feed OpenAPI into authorized API testing tools (e.g. Praetorian Hadrian) only within engagement scope.

---

## 9. Common pitfalls

- Assuming one crawl covers all user journeys (auth and role matter).
- Forgetting authenticated headers on gated APIs.
- Treating generated specs as a complete system contract.
- Inventing README-only flags (`grpc`, `--analyze-js`, …) on the v1.0.0 binary.
- Enabling `--dangerous-allow-private` outside controlled labs.
- Parsing the startup banner instead of `-o` artifacts.
- Expecting Chrome-free headless when `--headless` is set without a system browser.

---

## 10. Quick reference card

```bash
# Triage
vespasian scan https://target -o api.yaml

# Corpus two-stage
vespasian crawl https://target -o capture.json
vespasian generate rest capture.json -o openapi.yaml

# Import
vespasian import har session.har -o capture.json

# Lab
vespasian scan http://127.0.0.1:8080 --dangerous-allow-private -o api.yaml
```

Help & options: `Vespasian-CLI-Options.md` · Skill: `.cursor/skills/vespian/SKILL.md`
