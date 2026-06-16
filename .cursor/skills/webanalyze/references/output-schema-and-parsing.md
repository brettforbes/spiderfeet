# webanalyze Output Schema and Parsing

webanalyze reports detected technologies derived from signatures similar to the Wappalyzer ecosystem.

## Expected detection fields

| Field class | Meaning |
|---|---|
| Target identity | scanned URL/host |
| Technology name | product/framework/CMS identifier |
| Categories | taxonomy (CMS, JS framework, web server, analytics, etc.) |
| Version/confidence | optional detection strength and version |
| Evidence source | header, cookie, script URL, HTML pattern, meta tag |

## Parser workflow

1. Parse line/object according to selected output mode.
2. Normalize target host and technology name.
3. Store category list and confidence/version if present.
4. Keep raw evidence pointers for auditability.
5. Emit normalized records for nugget mapping.

## Text-mode fallback parsing

If JSON output is unavailable:

- parse deterministic `target -> technology` patterns,
- trim ANSI/log prefixes,
- preserve original line in `raw_evidence`.

## Example normalization record

```json
{
  "target": "https://shop.example.com",
  "host": "shop.example.com",
  "technology": "nginx",
  "categories": ["Web servers"],
  "version": "",
  "confidence": 100,
  "evidence": ["header:server"]
}
```
