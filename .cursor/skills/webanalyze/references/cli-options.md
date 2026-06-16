# webanalyze CLI Options

`webanalyze` releases vary; confirm exact flags with `webanalyze -h` for your build.

## Major option classes

| Class | Typical usage shape | Purpose |
|---|---|---|
| Single target scan | `-host <url>` | Fingerprint one web endpoint |
| Batch scan | list/targets file option | Fingerprint many hosts efficiently |
| Output mode | JSON/text flags by version | Choose parser-safe format |
| Timeout/transport | timeout/TLS/proxy flags | Improve reliability in noisy environments |
| Fingerprint data source | built-in/custom fingerprints | Extend coverage for private stacks |

## Examples by option class

```bash
# Single host
webanalyze -host https://example.com

# Alternate path scan
webanalyze -host https://example.com/login

# Batch (if your version supports target lists)
webanalyze -hosts hosts.txt

# JSON output (if supported)
webanalyze -host https://example.com -json
```

## Practical recommendations

- Always include explicit scheme (`http://` or `https://`).
- Scan at least one app path beyond `/` for framework-heavy apps.
- Prefer structured output for automation pipelines.
- Keep tool and fingerprint database versions pinned in repeatable workflows.
