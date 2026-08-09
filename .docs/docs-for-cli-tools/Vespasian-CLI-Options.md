# Vespasian CLI Options

Operator reference for **`vespasian`** **v1.0.0** ([praetorian-inc/vespasian](https://github.com/praetorian-inc/vespasian)). Prefer structured artifacts written with `-o` (`capture.json`, OpenAPI, GraphQL SDL, WSDL).

## SpiderFeet preferred commands

```bash
# One-step OpenAPI (auto API type)
vespasian scan https://app.example.com -o openapi.yaml

# Two-stage: capture then OpenAPI / GraphQL / WSDL
vespasian crawl https://app.example.com -o capture.json
vespasian generate rest capture.json -o openapi.yaml
vespasian generate graphql capture.json -o schema.graphql
vespasian generate wsdl capture.json -o service.wsdl

# Import existing proxy traffic
vespasian import burp traffic.xml -o capture.json
vespasian import har recording.har -o capture.json
vespasian import mitmproxy flows -o capture.json
```

| Field | Value |
|-------|-------|
| Version | **v1.0.0** (commit `f93dab002fb600e03a3c75ec3fac57a6606f79f3`, built `2026-04-03T04:27:30Z`) |
| Binary (WSL) | `/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian` |
| Binary (Windows path) | `C:\projects\spiderfeet\.tools\vespasian\vespasian` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_vespasian_help/*.txt` |
| Skill | `.cursor/skills/vespian/SKILL.md` |

> Flags below are from live `--help` on **v1.0.0** only. Do not invent options. Upstream README may document newer flags (`grpc`, `--analyze-js`, …) that are absent from this binary’s help.

---

## Captured help

Live help text captured from `/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian` via WSL on **2026-08-10**. Each block is the full stdout of the listed command. Nested files `import_burp_help.txt`, `import_har_help.txt`, `import_mitmproxy_help.txt`, `import_openapi_help.txt`, `import_graphql_help.txt`, `import_wsdl_help.txt` all match `import --help` (formats remain `burp`, `har`, `mitmproxy`). Nested `generate_openapi_help.txt`, `generate_graphql_help.txt`, `generate_wsdl_help.txt` all match `generate --help` (api-types remain `rest`, `wsdl`, `graphql`).

### Root (`vespasian --help`)

```text
Usage: vespasian <command> [flags]

API discovery tool for security assessments.

Flags:
  -h, --help         Show context-sensitive help.
      --no-banner    Suppress the startup banner

Commands:
  crawl <url> [flags]
    Crawl a web application to discover API endpoints

  import <format> <file> [flags]
    Import traffic capture from external sources

  generate <api-type> <capture> [flags]
    Generate API specifications from captured traffic

  scan <url> [flags]
    Full pipeline: crawl, classify, and generate specs

  version [flags]
    Show version information

Run "vespasian <command> --help" for more information on a command.
```

### `version` (`vespasian version` and `vespasian version --help`)

```text
vespasian 1.0.0 (commit: f93dab002fb600e03a3c75ec3fac57a6606f79f3, built: 2026-04-03T04:27:30Z)
```

```text
Usage: vespasian version [flags]

Show version information

Flags:
  -h, --help         Show context-sensitive help.
      --no-banner    Suppress the startup banner
```

### `crawl` (`vespasian crawl --help`)

```text
Usage: vespasian crawl <url> [flags]

Crawl a web application to discover API endpoints

Arguments:
  <url>    Target URL to crawl

Flags:
  -h, --help                   Show context-sensitive help.
      --no-banner              Suppress the startup banner

  -H, --header=HEADER,...      Custom headers (repeatable)
  -o, --output=STRING          Output file path
      --depth=3                Maximum crawl depth
      --max-pages=100          Maximum pages to crawl
      --timeout=10m            Maximum duration for the entire crawl
      --scope="same-origin"    Crawl scope
      --headless               Use headless browser
      --proxy=STRING           Proxy address for headless browser (e.g.,
                               http://127.0.0.1:8080). Note: TLS certificate
                               verification is disabled during crawls.
      --no-request-id          Disable automatic X-Vespasian-Request-Id header
  -v, --verbose                Enable verbose logging
```

### `import` (`vespasian import --help`)

```text
Usage: vespasian import <format> <file> [flags]

Import traffic capture from external sources

Arguments:
  <format>    Import format (burp, har, mitmproxy)
  <file>      Input file path

Flags:
  -h, --help             Show context-sensitive help.
      --no-banner        Suppress the startup banner

  -o, --output=STRING    Output file path
  -v, --verbose          Enable verbose logging
```

### `generate` (`vespasian generate --help`)

```text
Usage: vespasian generate <api-type> <capture> [flags]

Generate API specifications from captured traffic

Arguments:
  <api-type>    API type to generate (rest, wsdl, graphql)
  <capture>     Capture file path

Flags:
  -h, --help                       Show context-sensitive help.
      --no-banner                  Suppress the startup banner

  -o, --output=STRING              Output file path
      --confidence=0.5             Minimum confidence threshold
      --probe                      Enable endpoint probing
      --deduplicate                Deduplicate classified endpoints before
                                   probing
      --dangerous-allow-private    Disable SSRF protection for probes,
                                   allowing private/localhost targets. WARNING:
                                   Do not use on production systems.
  -v, --verbose                    Enable verbose logging
```

### `scan` (`vespasian scan --help`)

```text
Usage: vespasian scan <url> [flags]

Full pipeline: crawl, classify, and generate specs

Arguments:
  <url>    Target URL to scan

Flags:
  -h, --help                       Show context-sensitive help.
      --no-banner                  Suppress the startup banner

      --api-type="auto"            API type to generate (auto detects from
                                   traffic)
      --confidence=0.5             Minimum confidence threshold
      --probe                      Enable endpoint probing
      --deduplicate                Deduplicate classified endpoints before
                                   probing
      --dangerous-allow-private    Disable SSRF protection for probes,
                                   allowing private/localhost targets. WARNING:
                                   Do not use on production systems.
  -H, --header=HEADER,...          Custom headers (repeatable)
  -o, --output=STRING              Output file path
      --depth=3                    Maximum crawl depth
      --max-pages=100              Maximum pages to crawl
      --timeout=10m                Maximum duration for the entire crawl
      --scope="same-origin"        Crawl scope
      --headless                   Use headless browser
      --proxy=STRING               Proxy address for headless browser (e.g.,
                                   http://127.0.0.1:8080). Note: TLS certificate
                                   verification is disabled during crawls.
      --no-request-id              Disable automatic X-Vespasian-Request-Id
                                   header
  -v, --verbose                    Enable verbose logging
```

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

```bash
/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian --help
/mnt/c/projects/spiderfeet/.tools/vespasian/vespasian crawl --help
# …
```

---

## Synopsis

```
vespasian [--no-banner] <command> …

vespasian crawl <url> [flags]
vespasian import <burp|har|mitmproxy> <file> [-o PATH] [-v]
vespasian generate <rest|wsdl|graphql> <capture> [flags]
vespasian scan <url> [flags]
vespasian version
```

---

## Options reference (captured binary)

### Global

| Flag | Description |
|------|-------------|
| `-h, --help` | Context-sensitive help |
| `--no-banner` | Suppress the startup banner |

### `crawl`

| Flag | Default | Description |
|------|---------|-------------|
| `<url>` | *(required)* | Target URL to crawl |
| `-H, --header` | — | Custom headers (repeatable) |
| `-o, --output` | — | Output file path (use `capture.json`) |
| `--depth` | `3` | Maximum crawl depth |
| `--max-pages` | `100` | Maximum pages to crawl |
| `--timeout` | `10m` | Maximum duration for the entire crawl |
| `--scope` | `same-origin` | Crawl scope |
| `--headless` | — | Use headless browser |
| `--proxy` | — | Proxy for headless browser; TLS verification disabled during crawls (per help) |
| `--no-request-id` | — | Disable automatic `X-Vespasian-Request-Id` |
| `-v, --verbose` | — | Verbose logging |

### `import`

| Flag / arg | Description |
|------------|-------------|
| `<format>` | `burp`, `har`, or `mitmproxy` |
| `<file>` | Input path |
| `-o, --output` | Capture output path |
| `-v, --verbose` | Verbose logging |

### `generate`

| Flag / arg | Default | Description |
|------------|---------|-------------|
| `<api-type>` | *(required)* | `rest` (OpenAPI), `wsdl`, or `graphql` (SDL) |
| `<capture>` | *(required)* | Capture file path |
| `-o, --output` | — | Spec output path |
| `--confidence` | `0.5` | Minimum confidence threshold |
| `--probe` | — | Enable endpoint probing |
| `--deduplicate` | — | Deduplicate classified endpoints before probing |
| `--dangerous-allow-private` | — | Disable SSRF protection for probes (private/localhost). Help warns: do not use on production systems |
| `-v, --verbose` | — | Verbose logging |

### `scan`

| Flag | Default | Description |
|------|---------|-------------|
| `<url>` | *(required)* | Target URL |
| `--api-type` | `auto` | API type (`auto` detects from traffic; also use `rest` / `graphql` / `wsdl` when forcing type) |
| `--confidence` | `0.5` | Minimum confidence threshold |
| `--probe` | — | Enable endpoint probing |
| `--deduplicate` | — | Deduplicate before probing |
| `--dangerous-allow-private` | — | Disable SSRF protection for probes |
| `-H, --header` | — | Custom headers (repeatable) |
| `-o, --output` | — | Spec output path |
| `--depth` | `3` | Max crawl depth |
| `--max-pages` | `100` | Max pages |
| `--timeout` | `10m` | Crawl duration limit |
| `--scope` | `same-origin` | Crawl scope |
| `--headless` | — | Use headless browser |
| `--proxy` | — | Proxy for headless browser |
| `--no-request-id` | — | Disable `X-Vespasian-Request-Id` |
| `-v, --verbose` | — | Verbose logging |

---

## Structured outputs

v1.0.0 has **no** dedicated `--json` / JSONL findings flag. Structured examination artifacts are the files produced with `-o`:

| Command | Typical output | Structured form |
|---------|----------------|-----------------|
| `crawl` / `import` | `capture.json` | JSON capture of observed requests |
| `generate rest` / REST `scan` | `openapi.yaml` | OpenAPI 3.x (YAML or JSON) |
| `generate graphql` | `schema.graphql` | GraphQL SDL |
| `generate wsdl` | `service.wsdl` | WSDL XML |

---

## Examples

```bash
vespasian scan https://app.example.com -o api.yaml
vespasian scan https://app.example.com --api-type graphql -o schema.graphql
vespasian crawl https://app.example.com -H "Authorization: Bearer TOKEN" -o capture.json
vespasian generate rest capture.json --probe --deduplicate --confidence 0.7 -o openapi.yaml
vespasian scan http://localhost:3000 --dangerous-allow-private -o api.yaml
vespasian scan https://app.example.com --proxy http://127.0.0.1:8080 -o api.yaml
vespasian --no-banner version
```

---

## README / newer-build drift

Documented in upstream README or newer sources but **not** present in Captured help for this **v1.0.0** binary — verify after upgrading before relying on them:

- `--api-type grpc` / `.proto` generation
- `--headless=false` net/http backend wording
- `--proxy-insecure`, `--analyze-js`, `--fetch-sourcemaps`, `--merge-slugs`, `--target-url`, gRPC TLS skip flags
- Additional generate flags (`--proxy` on generate, etc.)

When Captured help and README disagree, **Captured help wins** for the installed binary.

---

## See also

- `.docs/docs-for-cli-tools/Vespasian-Zero-to-Hero.md`
- `.cursor/skills/vespian/SKILL.md`
- `.cursor/skills/vespian/references/cli-options.md`
