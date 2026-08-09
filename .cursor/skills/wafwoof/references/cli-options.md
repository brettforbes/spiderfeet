# WAFWOOF CLI Options

Binary: `wafw00f` (package name `wafw00f`, skill folder `wafwoof`).

SpiderFeet default:

```bash
wafw00f -a -o- -f json <URL>
```

## Captured help

Live capture from **wafw00f v2.4.2** at `C:\projects\spiderfeet\.venv\Scripts\wafw00f.exe` on **2026-08-10**.

```text
Usage: wafw00f url1 [url2 [url3 ... ]]

example: wafw00f http://www.victim.org/

Options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbosity, multiple -v options increase
                        verbosity
  -a, --findall         Find all WAFs which match the signatures, do not stop
                        testing on the first one
  -r, --noredirect      Do not follow redirections given by 3xx responses
  -t TEST, --test=TEST  Test for one specific WAF (use --list to get names,
                        quote names with spaces e.g. "AireeCDN (Airee)")
  -o OUTPUT, --output=OUTPUT
                        Write output to csv, json or text file depending on
                        file extension. For stdout, specify - as filename.
  -f FORMAT, --format=FORMAT
                        Force output format to csv, json or text.
  -i INPUT, --input-file=INPUT
                        Read targets from a file. Input format can be csv,
                        json or text. For csv and json, a `url` column name or
                        element is required.
  -l, --list            List all WAFs that WAFW00F is able to detect
  -p PROXY, --proxy=PROXY
                        Use an HTTP proxy to perform requests, examples:
                        http://hostname:8080, socks5://hostname:1080,
                        http://user:pass@hostname:8080
  -V, --version         Print out the current version of WafW00f and exit.
  -H HEADERS, --headers=HEADERS
                        Pass custom headers via a text file to overwrite the
                        default header set.
  -T TIMEOUT, --timeout=TIMEOUT
                        Set the timeout for the requests.
  --no-colors           Disable ANSI colors in output.
```

Operator copy: `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md`

## Synopsis

```
wafw00f [options] url1 [url2 ...]
wafw00f [options] -i <input-file>
```

## Target input

| Option | Description |
|--------|-------------|
| `url` (positional) | One or more URLs. Scheme added if missing (`https://`). |
| `-i`, `--input-file <file>` | Bulk input. Format by extension: `.json` (array of `{"url":...}`), `.csv` (`url` column), or plain text (one URL per line). |

## Detection behaviour

| Option | Description |
|--------|-------------|
| `-a`, `--findall` | Test all matching WAF signatures; do not stop at first hit. **SpiderFeet default.** |
| `-t`, `--test <name>` | Test only one WAF product. Name must match `wafw00f -l` entry (quote names with spaces). |
| `-r`, `--noredirect` | Do not follow 3xx redirects. |
| `-T`, `--timeout <sec>` | Per-request timeout. |

## Output

| Option | Description |
|--------|-------------|
| `-o`, `--output <file>` | Write results to file. Use `-` for stdout. Extension `.json`/`.csv`/`.txt` selects format. |
| `-f`, `--format <fmt>` | Force format: `json`, `csv`, or `text`. Use with `-o -` for JSON on stdout. **SpiderFeet: `-o- -f json`.** |
| `--no-colors` | Disable ANSI colours (useful when capturing logs). |

## HTTP client

| Option | Description |
|--------|-------------|
| `-p`, `--proxy <url>` | HTTP/SOCKS proxy, e.g. `http://host:8080`, `socks5://host:1080`, `http://user:pass@host:8080`. |
| `-H`, `--headers <file>` | Custom headers file. One `Header: value` per line; **replaces** default Chrome-on-Windows set. |

## Information

| Option | Description |
|--------|-------------|
| `-l`, `--list` | List all detectable WAF products and manufacturers. |
| `-V`, `--version` | Print version and license. |
| `-h`, `--help` | Help text. |
| `-v`, `--verbose` | Increase verbosity (repeat for more: `-v -v`). |

## Attack probes (internal)

wafw00f issues normal requests plus crafted XSS, SQLi, LFI, XXE, and command-injection style probes to elicit WAF-specific responses. Expect IDS/WAF alerts on target.

## JSON stdout pattern

```bash
wafw00f -a -o- -f json https://example.com
```

When `-o -` is set, human-readable art may appear on stderr; JSON array prints to stdout.

## SpiderFeet module options

| Option | Description |
|--------|-------------|
| `wafw00f_path` | Optional path to `wafw00f` executable |
| `python_path` | Python for script install if not using PATH binary |

Resolution order: `shutil.which('wafw00f')` then configured path.

## Per-flag examples

```bash
wafw00f -h
wafw00f -V
wafw00f -l
wafw00f -v -v -a -o- -f json https://example.com
wafw00f -a -o- -f json https://example.com
wafw00f -o- -f json https://example.com
wafw00f -t "Cloudflare (Cloudflare Inc.)" -o- -f json https://example.com
wafw00f -r -a -o- -f json https://example.com
wafw00f -T 15 -a -o- -f json https://example.com
wafw00f --no-colors -a -o- -f json https://example.com
wafw00f -a -p http://127.0.0.1:8080 -o- -f json https://example.com
wafw00f -a -H headers.txt -o- -f json https://example.com
wafw00f -a -i targets.json -o- -f json
wafw00f -a -o results.json https://example.com
wafw00f -a -o results.csv -f csv https://example.com
```
