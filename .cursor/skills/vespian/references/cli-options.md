# Vespasian CLI Options

Invocation: **`vespasian`** (Praetorian; case-sensitive). Skill folder name: `vespian`.

SpiderFeet formal examination defaults:

```bash
# One-step structured OpenAPI (or GraphQL/WSDL via --api-type)
vespasian scan <url> -o openapi.yaml

# Two-stage: retain capture, then generate
vespasian crawl <url> -o capture.json
vespasian generate rest capture.json -o openapi.yaml
```

| Field | Value |
|-------|-------|
| Binary (WSL) | `/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian` |
| Binary (Windows path) | `C:\projects\spiderfeet\.tools\vespasian\vespasian` |
| Version | **v1.0.0** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_vespasian_help/*.txt` |

> Flags below are from live `--help` on **v1.0.0** only. Do not invent options from upstream README (`grpc`, `--analyze-js`, `--proxy-insecure`, …) until they appear in Captured help for the binary in use.

## Captured help

Live help text from `/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian` via WSL on **2026-08-10**. Nested `import_*` / `generate_*` stubs under `.tmp_vespasian_help/` duplicate the parent command help (import still only documents `burp`, `har`, `mitmproxy`; generate still only documents `rest`, `wsdl`, `graphql`). Full verbatim blocks: `.docs/docs-for-cli-tools/Vespasian-CLI-Options.md` § Captured help.

### Re-capture

```powershell
New-Item -ItemType Directory -Force -Path .tmp_vespasian_help | Out-Null
$bin = "/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian"
wsl bash -lc "$bin --help" | Out-File -Encoding utf8 .tmp_vespasian_help/root_help.txt
wsl bash -lc "$bin crawl --help" | Out-File -Encoding utf8 .tmp_vespasian_help/crawl_help.txt
wsl bash -lc "$bin import --help" | Out-File -Encoding utf8 .tmp_vespasian_help/import_help.txt
wsl bash -lc "$bin generate --help" | Out-File -Encoding utf8 .tmp_vespasian_help/generate_help.txt
wsl bash -lc "$bin scan --help" | Out-File -Encoding utf8 .tmp_vespasian_help/scan_help.txt
wsl bash -lc "$bin version --help" | Out-File -Encoding utf8 .tmp_vespasian_help/version_help.txt
wsl bash -lc "$bin version" | Out-File -Encoding utf8 .tmp_vespasian_help/version.txt
```

## Command tree (v1.0.0)

| Command | Role |
|---------|------|
| `vespasian crawl <url>` | Capture traffic → `capture.json` |
| `vespasian import <format> <file>` | Import Burp / HAR / mitmproxy → capture |
| `vespasian generate <api-type> <capture>` | Spec from capture (`rest` / `graphql` / `wsdl`) |
| `vespasian scan <url>` | Full pipeline: crawl + classify + generate |
| `vespasian version` | Version string |

Global flags (all commands): `-h/--help`, `--no-banner`.

## Options by command (from Captured help)

### Global

| Flag | Description |
|------|-------------|
| `-h, --help` | Context-sensitive help |
| `--no-banner` | Suppress startup banner |

### `crawl <url>`

| Flag | Default (help) | Description |
|------|----------------|-------------|
| `-H, --header` | — | Custom headers (repeatable) |
| `-o, --output` | — | Output file path |
| `--depth` | `3` | Maximum crawl depth |
| `--max-pages` | `100` | Maximum pages to crawl |
| `--timeout` | `10m` | Maximum duration for the entire crawl |
| `--scope` | `same-origin` | Crawl scope |
| `--headless` | — | Use headless browser |
| `--proxy` | — | Proxy for headless browser (e.g. `http://127.0.0.1:8080`); help notes TLS verification disabled during crawls |
| `--no-request-id` | — | Disable automatic `X-Vespasian-Request-Id` header |
| `-v, --verbose` | — | Verbose logging |

### `import <format> <file>`

| Argument / flag | Description |
|-----------------|-------------|
| `<format>` | `burp`, `har`, or `mitmproxy` |
| `<file>` | Input file path |
| `-o, --output` | Output file path |
| `-v, --verbose` | Verbose logging |

### `generate <api-type> <capture>`

| Argument / flag | Default (help) | Description |
|-----------------|----------------|-------------|
| `<api-type>` | — | `rest`, `wsdl`, or `graphql` |
| `<capture>` | — | Capture file path |
| `-o, --output` | — | Output file path |
| `--confidence` | `0.5` | Minimum confidence threshold |
| `--probe` | — | Enable endpoint probing |
| `--deduplicate` | — | Deduplicate classified endpoints before probing |
| `--dangerous-allow-private` | — | Disable SSRF protection for probes (private/localhost). Warning in help: do not use on production systems |
| `-v, --verbose` | — | Verbose logging |

### `scan <url>`

Combines crawl + generate flags:

| Flag | Default (help) | Description |
|------|----------------|-------------|
| `--api-type` | `auto` | API type to generate (auto detects from traffic) |
| `--confidence` | `0.5` | Minimum confidence threshold |
| `--probe` | — | Enable endpoint probing |
| `--deduplicate` | — | Deduplicate before probing |
| `--dangerous-allow-private` | — | Disable SSRF protection for probes |
| `-H, --header` | — | Custom headers (repeatable) |
| `-o, --output` | — | Output file path |
| `--depth` | `3` | Max crawl depth |
| `--max-pages` | `100` | Max pages |
| `--timeout` | `10m` | Crawl duration limit |
| `--scope` | `same-origin` | Crawl scope |
| `--headless` | — | Use headless browser |
| `--proxy` | — | Proxy for headless browser |
| `--no-request-id` | — | Disable `X-Vespasian-Request-Id` |
| `-v, --verbose` | — | Verbose logging |

### `version`

Only `-h/--help` and `--no-banner`.

## Structured outputs (prefer these)

There is **no** separate `--json` findings flag on v1.0.0. Structured artifacts are the files you write with `-o`:

| Stage | Typical `-o` | Format |
|-------|--------------|--------|
| `crawl` / `import` | `capture.json` | Vespasian capture (JSON request array) |
| `generate rest` / `scan` (REST) | `openapi.yaml` | OpenAPI 3.x |
| `generate graphql` / `scan --api-type graphql` | `schema.graphql` | GraphQL SDL |
| `generate wsdl` / `scan --api-type wsdl` | `service.wsdl` | WSDL XML |

## README / newer-build drift (not in Captured help)

Upstream README may document additional flags/types (`grpc`, `--headless=false`, `--proxy-insecure`, `--analyze-js`, `--merge-slugs`, …). On **this** v1.0.0 binary they did **not** appear in `--help`. Build from newer source and re-capture help before documenting them as available.

## See also

- `.docs/docs-for-cli-tools/Vespasian-CLI-Options.md` — full Captured help text
- [`output-and-parsing.md`](output-and-parsing.md)
- [`tactics.md`](tactics.md)
