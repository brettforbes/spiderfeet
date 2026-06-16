# WAFWOOF CLI Options

Binary: `wafw00f` (package name `wafw00f`, skill folder `wafwoof`).

SpiderFeet default:

```bash
wafw00f -a -o- -f json <URL>
```

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
| `-T`, `--timeout <sec>` | Per-request timeout (default 7). |

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

When `-o -` is set, human-readable art may be suppressed on stderr; JSON array prints to stdout.

## SpiderFeet module options

| Option | Description |
|--------|---------|
| `wafw00f_path` | Optional path to `wafw00f` executable |
| `python_path` | Python for script install if not using PATH binary |

Resolution order: `shutil.which('wafw00f')` then configured path.

## Examples

```bash
# SpiderFeet equivalent
wafw00f -a -o- -f json https://example.com

# Faster single-match
wafw00f -o- -f json https://example.com

# Verbose debug
wafw00f -v -v -a -o- -f json https://example.com

# Write file
wafw00f -a -o scan.json https://example.com

# CSV export
wafw00f -a -o scan.csv https://example.com
```
