# webanalyze CLI Options

Invocation: **`webanalyze`**. SpiderFeet formal examination defaults:

```bash
webanalyze -host https://example.com -output json -silent
webanalyze -hosts hosts.txt -output json -silent
```

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe` |
| Release zip (same dir) | `webanalyze_Windows_x86_64.zip` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_webanalyze_help/help_h.txt`, `help_long.txt`, `version.txt` |

> **No `-version` / `--version`.** Live binary: `flag provided but not defined: -version`. Do not invent one. Banner version appears on stderr when not `-silent`.

> Flags below are from live `-h` only. Do not invent options (there is **no** `-json` flag — use `-output json`).

## Captured help

Live help from `.tools/webanalyze/webanalyze.exe` on **2026-08-10** (`-h` and long help are identical):

```text
Usage of C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe:
  -apps string
    	technologies definition file (default "technologies.json")
  -crawl int
    	links to follow from the root page (default 0)
  -host string
    	single host to test
  -hosts string
    	filename with hosts, one host per line.
  -output string
    	output format (stdout|csv|json) (default "stdout")
  -redirect
    	follow http redirects (default false)
  -search
    	searches all urls with same base domain (i.e. example.com and sub.example.com) (default true)
  -silent
    	avoid printing header (default false)
  -update
    	update technologies file to current dir
  -worker int
    	number of worker (default 4)
```

### Re-capture

```powershell
$out = "C:\projects\spiderfeet\.tmp_webanalyze_help"
New-Item -ItemType Directory -Force -Path $out | Out-Null
& "C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe" -h 2>&1 | Set-Content "$out\help_h.txt"
```

## Synopsis

```
webanalyze -update
webanalyze -host <url|hostname> [flags]
webanalyze -hosts <file> [flags]
```

Requires `-update` alone, or `-host` / `-hosts` with a resolvable `technologies.json` (via `-apps` or lookup folders).

## Options reference

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-apps` | string | `technologies.json` | Technologies definition file |
| `-crawl` | int | `0` | Number of links to follow from the root page |
| `-host` | string | _(empty)_ | Single host/URL to test |
| `-hosts` | string | _(empty)_ | File with hosts, one per line |
| `-output` | string | `stdout` | Output format: `stdout` \| `csv` \| `json` |
| `-redirect` | bool | `false` | Follow HTTP redirects |
| `-search` | bool | `true` | Search URLs with the same base domain |
| `-silent` | bool | `false` | Suppress stderr header banner |
| `-update` | bool | `false` | Download/update `technologies.json` into the current directory |
| `-worker` | int | `4` | Worker concurrency |

### Bool defaults note

- Enable redirect: `-redirect`
- Disable same-base-domain search: `-search=false` (Go flag form; default is already true)

## Option classes and examples

### Definitions update

```bash
webanalyze -update
webanalyze -update -silent
```

### Single target

```bash
webanalyze -host https://example.com -output json -silent
webanalyze -host example.com -output json -silent   # becomes http://example.com
```

### Batch targets

```bash
webanalyze -hosts hosts.txt -output json -silent -worker 8
```

### Crawl / redirect / search

```bash
webanalyze -host https://shop.example.com -crawl 2 -redirect -output json -silent
webanalyze -host https://shop.example.com/login -search=false -output json -silent
```

### Custom apps file

```bash
webanalyze -apps C:\path\to\technologies.json -host https://example.com -output json -silent
```

### Human stdout / CSV

```bash
webanalyze -host https://example.com -crawl 1
webanalyze -host https://example.com -output csv -silent
```

## Streams

| Stream | Content |
|--------|---------|
| **stdout** | Findings: human table (`stdout`), CSV rows, or JSON lines (`json`) |
| **stderr** | Header banner (`:: webanalyze …`), `-update` log line, per-host `error:` lines |

For corpus capture: `-output json -silent` and collect stdout; keep stderr sidecar for errors.

## Technologies file lookup

When `-apps` is a relative path, webanalyze searches:

1. Current working directory
2. Directory of the executable
3. User home directory

## Practical recommendations

- Prefer **`-output json`** for SpiderFeet (structured-first).
- Run **`-update`** before first use and when definitions are >1 week old.
- Prefer explicit **`https://`** targets.
- Opt in to **`-redirect`** for sites that bounce to a final app URL.
- Use **`-silent`** for clean NDJSON pipelines.
