# webanalyze CLI Options

Operator-oriented option guide for `webanalyze`. Exact switches may differ by build; validate with `webanalyze -h`.

## Standard option classes

| Class | Typical usage |
|---|---|
| Target URL | `-host <url>` |
| Batch targets | list file/hosts option |
| Output mode | JSON/text switch by version |
| Runtime controls | timeout, TLS, proxy (if available) |

## Advanced option classes

| Class | Use case |
|---|---|
| Custom fingerprints | Extend detections beyond defaults |
| Fingerprint DB updates | Keep signatures current |
| Debug/verbose output | Inspect why detections occurred or failed |

## Examples by option class

```bash
# Single URL
webanalyze -host https://example.com

# App path
webanalyze -host https://example.com/login

# Batch mode (if available)
webanalyze -hosts hosts.txt

# JSON output (if available)
webanalyze -host https://example.com -json
```

## Parsing and graph conversion reminder

Normalize detections into:
- `nodes[]`: `INTERNET_NAME`, `WEBSERVER_TECHNOLOGY`
- `edges[]`: `uses_technology`

Reference: `.cursor/skills/webanalyze/references/nugget-mapping.md`.
