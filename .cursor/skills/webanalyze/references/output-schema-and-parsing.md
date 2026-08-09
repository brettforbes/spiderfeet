# webanalyze Output Schema and Parsing

Prefer **`-output json`**. Do not use native stdout text as the graph source when JSON is available.

## Capture family

| Mode | Artifact | SpiderFeet role |
|------|----------|-----------------|
| `-output json` | NDJSON (one object per host line) | **Primary** — normalize to a single JSON bundle with `records[]` at harvest |
| `-output csv` | CSV with header `Host,Category,App,Version` | Triage only |
| `-output stdout` (default) | Human table | Exploration only |

## JSON shape (`-output json`)

Each successful host emits **one JSON object followed by a newline** (NDJSON), not a wrapping array.

Top-level fields (CLI marshal in `cmd/webanalyze/main.go`):

| Field | Type | Meaning |
|-------|------|---------|
| `hostname` | string | Scanned URL as resolved/normalized by the tool |
| `matches` | array | Detected technologies (may be empty) |

Each `matches[]` element:

| Field | Type | Meaning |
|-------|------|---------|
| `app_name` | string | Technology name (primary identity) |
| `version` | string | Detected version or `""` |
| `matches` | array of string arrays | Regex/evidence hit groups |
| `app` | object | Embedded app definition snapshot |

Useful `app` subfields when present:

| Field | Meaning |
|-------|---------|
| `cats` | Category id strings |
| `category_names` | Human category labels (e.g. `CDN`, `CMS`) |
| `website` | Vendor/product URL from definitions |
| `implies` | Implied technology names from definitions |
| `headers` / `html` / `scripts` / `cookies` / `meta` / `url` | Signature source material (definition-side) |

### Live sample (2026-08-10)

Command:

```bash
webanalyze -host https://example.com -output json -silent -search=false
```

Stdout (single line; pretty-printed here):

```json
{
  "hostname": "https://example.com",
  "matches": [
    {
      "app": {
        "cats": ["31"],
        "category_names": ["CDN"],
        "cookies": { "__cfduid": "" },
        "headers": {
          "Server": "^cloudflare$",
          "cf-cache-status": "",
          "cf-ray": ""
        },
        "meta": { "image": ["//cdn\\.cloudflare"] },
        "html": [""],
        "scripts": [""],
        "url": [""],
        "website": "https://www.cloudflare.com",
        "implies": [""]
      },
      "app_name": "Cloudflare",
      "matches": [["a2885a8e0a90cd77-SYD"], ["cloudflare"], ["HIT"]],
      "version": ""
    }
  ]
}
```

## Corpus bundle normalization

At harvest, parse stdout lines into `list[dict]`, skip non-JSON lines, then write a single-root bundle:

```json
{
  "schema": "webanalyze_host_v1",
  "tool": "webanalyze",
  "command": "…",
  "started_at": "…",
  "duration_s": 0,
  "exit_code": 0,
  "record_count": 1,
  "stderr_banner": "",
  "records": [
    { "hostname": "https://example.com", "matches": [ ] }
  ]
}
```

Do **not** store raw `.jsonl` as the CLI Profiling Structured artifact.

## CSV shape (`-output csv`)

Header row (always written when mode is csv):

```text
Host,Category,App,Version
```

One data row per match. Category cells may contain comma-joined names.

## Stdout human shape

```text
https://example.com (0.4s):
    Cloudflare,  (CDN)
```

Empty match sets still print the host line and a blank indented line.

## Errors

Failed retrieves are written to **stderr**:

```text
https://bad.example error: Failed to retrieve: …
```

No JSON object is emitted for that host on success-path stdout. Include stderr in examination evidence; structured bundle should carry `exit_code` and stderr text.

## Parser workflow

1. Prefer `-output json -silent`.
2. Split stdout by lines; `json.loads` each non-empty line.
3. Normalize host from `hostname` (strip scheme/path for `INTERNET_NAME` when mapping).
4. For each match, keep `app_name`, `version`, `app.category_names`, and raw match evidence.
5. Bundle into `records[]` before graph derivation.
