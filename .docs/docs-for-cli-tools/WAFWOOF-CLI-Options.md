# WAFWOOF CLI Options

Binary: `wafw00f`. SpiderFeet invocation:

```bash
wafw00f -a -o- -f json <URL>
```

## Usage

```
wafw00f [options] url1 [url2 ...]
```

## Options

| Short | Long | Description |
|-------|------|-------------|
| `-h` | `--help` | Show help and exit |
| `-v` | `--verbose` | Verbose logging (repeat for more detail) |
| `-a` | `--findall` | Find all matching WAF signatures; do not stop at first |
| `-r` | `--noredirect` | Do not follow HTTP redirects |
| `-t` | `--test` | Test for one specific WAF (name from `--list`) |
| `-o` | `--output` | Output file; use `-` for stdout |
| `-f` | `--format` | Force `json`, `csv`, or `text` |
| `-i` | `--input-file` | Input file (`json`/`csv`/`text`) with URLs |
| `-l` | `--list` | List all detectable WAF products |
| `-p` | `--proxy` | Proxy URL (`http://`, `socks5://`, auth supported) |
| `-H` | `--headers` | Custom headers file (overwrites defaults) |
| `-T` | `--timeout` | Request timeout in seconds (default: 7) |
| `-V` | `--version` | Print version |
| | `--no-colors` | Disable coloured terminal output |

## Output formats

| Combination | Result |
|-------------|--------|
| `-o- -f json` | JSON array on stdout (SpiderFeet) |
| `-o out.json` | JSON file (by extension) |
| `-o out.csv` | CSV file |
| `-o out.txt` | Human-readable text |

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

# Save JSON file
wafw00f -a -o results.json https://example.com
```

## SpiderFeet module configuration

| Option | Description |
|--------|-------------|
| `wafw00f_path` | Optional explicit path to executable |
| `python_path` | Python interpreter if running from source checkout |

## See also

- `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md`
- `.cursor/skills/wafwoof/SKILL.md`
