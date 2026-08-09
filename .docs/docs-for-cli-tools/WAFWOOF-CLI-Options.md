# WAFWOOF CLI Options

Binary: `wafw00f` (package and executable name; three zeros). SpiderFeet invocation:

```bash
wafw00f -a -o- -f json <URL>
```

## Captured help

Live capture from **wafw00f v2.4.2** at `C:\projects\spiderfeet\.venv\Scripts\wafw00f.exe` on **2026-08-10**. Not present under `.tools/` or WSL PATH on this host.

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

### Re-capture

```powershell
C:\projects\spiderfeet\.venv\Scripts\wafw00f.exe --help
C:\projects\spiderfeet\.venv\Scripts\wafw00f.exe --version
```

```bash
wafw00f --help
wafw00f --version
pip install wafw00f   # if missing
```

## Synopsis

```
wafw00f [options] url1 [url2 ...]
wafw00f [options] -i <input-file>
```

## Options reference

| Short | Long | Description |
|-------|------|-------------|
| `-h` | `--help` | Show help and exit |
| `-v` | `--verbose` | Verbose logging (repeat for more detail: `-v -v`) |
| `-a` | `--findall` | Find all matching WAF signatures; do not stop at first — **SpiderFeet default** |
| `-r` | `--noredirect` | Do not follow HTTP redirects |
| `-t` | `--test` | Test for one specific WAF (name from `--list`; quote names with spaces) |
| `-o` | `--output` | Output file; use `-` for stdout |
| `-f` | `--format` | Force `json`, `csv`, or `text` |
| `-i` | `--input-file` | Input file (`json`/`csv`/`text`) with URLs |
| `-l` | `--list` | List all detectable WAF products |
| `-p` | `--proxy` | Proxy URL (`http://`, `socks5://`, auth supported) |
| `-H` | `--headers` | Custom headers file (**overwrites** default Chrome-on-Windows set) |
| `-T` | `--timeout` | Request timeout in seconds |
| `-V` | `--version` | Print version and license |
| | `--no-colors` | Disable coloured terminal output |

## Output formats

| Combination | Result |
|-------------|--------|
| `-o- -f json` | JSON array on stdout (SpiderFeet) |
| `-o out.json` | JSON file (by extension) |
| `-o out.csv` | CSV file |
| `-o out.txt` | Human-readable text |
| `-o out.csv -f csv` | Force CSV regardless of extension |

## Input file formats (`-i`)

| Extension | Format |
|-----------|--------|
| `.json` | Array of objects with `url` key |
| `.csv` | Column named `url` |
| other | One URL per line |

## Examples

```bash
# SpiderFeet default
wafw00f -a -o- -f json https://example.com

# List products
wafw00f -l

# Single-vendor test
wafw00f -t "AWS Elastic Load Balancer (Amazon)" -o- -f json https://example.com

# Proxy + verbose
wafw00f -v -a -p http://127.0.0.1:8080 -o- -f json https://example.com

# No redirect
wafw00f -r -a -o- -f json https://example.com

# Custom headers + longer timeout
wafw00f -T 15 -H headers.txt -a -o- -f json https://example.com

# Bulk JSON input
wafw00f -a -i targets.json -o- -f json

# Save JSON file
wafw00f -a -o results.json https://example.com
```

## SpiderFeet module configuration

| Option | Description |
|--------|-------------|
| `wafw00f_path` | Optional explicit path to executable |
| `python_path` | Python interpreter if running from source checkout |

Resolution order: `shutil.which('wafw00f')` then configured path. Module command: `wafw00f -a -o- -f json <url>`.

## See also

- `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md`
- `.cursor/skills/wafwoof/SKILL.md`
- `modules/sfp_tool_wafw00f.py`
