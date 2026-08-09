# webanalyze CLI Options

Operator reference for **webanalyze** ([rverton/webanalyze](https://github.com/rverton/webanalyze)). Prefer structured JSON for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
webanalyze -host https://example.com -output json -silent
webanalyze -hosts hosts.txt -output json -silent
```

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe` |
| Release zip (same dir) | `webanalyze_Windows_x86_64.zip` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_webanalyze_help/*.txt` |

> **No `-version` / `--version`.** Live binary rejects `-version` (`flag provided but not defined`). Identify capability with `-h` and the stderr banner when not `-silent`.  
> Flags below are from live `-h` only — do not invent options. There is **no** `-json` flag; use **`-output json`**.

---

## Captured help

Live help text captured from `.tools/webanalyze/webanalyze.exe` on **2026-08-10** (`-h` / long help identical):

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
$bin = "C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe"
$out = "C:\projects\spiderfeet\.tmp_webanalyze_help"
New-Item -ItemType Directory -Force -Path $out | Out-Null
& $bin -h 2>&1 | Set-Content "$out\help_h.txt"
& $bin -version 2>&1 | Set-Content "$out\version.txt"   # expected: flag not defined
```

---

## Synopsis

```
webanalyze -update
webanalyze -host <url|hostname> [flags]
webanalyze -hosts <file> [flags]
```

Without `-update`, a scan requires `-host` or `-hosts` plus a findable `technologies.json`.

---

## Options reference

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-apps` | string | `technologies.json` | Technologies definition file |
| `-crawl` | int | `0` | Links to follow from the root page |
| `-host` | string | | Single host to test |
| `-hosts` | string | | Filename with hosts, one host per line |
| `-output` | string | `stdout` | Output format: `stdout` \| `csv` \| `json` |
| `-redirect` | bool | `false` | Follow HTTP redirects |
| `-search` | bool | `true` | Search URLs with the same base domain |
| `-silent` | bool | `false` | Avoid printing header |
| `-update` | bool | `false` | Update technologies file to current directory |
| `-worker` | int | `4` | Number of workers |

### Bool usage

```bash
webanalyze -host https://example.com -redirect -output json -silent
webanalyze -host https://example.com -search=false -output json -silent
```

---

## Standard option classes

| Class | Flags | Typical usage |
|-------|-------|---------------|
| Target (single) | `-host` | One URL or hostname |
| Target (batch) | `-hosts` | File, one host per line |
| Output | `-output`, `-silent` | Prefer `json` + `-silent` for automation |
| Crawl / redirect | `-crawl`, `-redirect`, `-search` | Deepen or constrain link following |
| Definitions | `-update`, `-apps` | Refresh or point at `technologies.json` |
| Concurrency | `-worker` | Parallel hosts (default 4) |

---

## Examples by option class

### Definitions

```bash
cd C:\projects\spiderfeet\.tools\webanalyze
webanalyze -update
```

### Single URL (structured)

```bash
webanalyze -host https://example.com -output json -silent
```

### Path-aware

```bash
webanalyze -host https://shop.example.com/login -search=false -output json -silent
```

### Batch

```bash
webanalyze -hosts hosts.txt -output json -silent -worker 8
```

### Crawl + redirects

```bash
webanalyze -host https://shop.example.com -crawl 2 -redirect -output json -silent
```

### Custom apps path

```bash
webanalyze -apps C:\projects\spiderfeet\.tools\webanalyze\technologies.json -host https://example.com -output json -silent
```

### Human / CSV (not for formal graph source when JSON exists)

```bash
webanalyze -host https://example.com -crawl 1
webanalyze -host https://example.com -output csv -silent
```

---

## Streams and JSON notes

- **stdout:** findings (`json` = one object per host line; fields `hostname`, `matches`).
- **stderr:** banner, update logs, `<host> error: …` lines.
- Bare hostnames get scheme **`http://`** if omitted — prefer explicit `https://`.
- Relative `-apps` lookup: `./`, executable directory, home.

---

## Parsing and graph conversion reminder

Normalize JSON detections into:

- `nodes[]`: `INTERNET_NAME`, `WEBSERVER_TECHNOLOGY`
- `edges[]`: `had` (host → technology)

Reference: `.cursor/skills/webanalyze/references/nugget-mapping.md`.
