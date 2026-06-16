# Vespasian CLI Options

## Core commands

- `vespasian scan <url>` - crawl + classify + generate in one step.
- `vespasian crawl <url>` - capture traffic only.
- `vespasian import <burp|har|mitmproxy> <file>` - convert existing captures.
- `vespasian generate <rest|graphql|wsdl> <capture-file>` - generate spec from capture.

## High-value flags

- `--api-type auto|rest|graphql|wsdl` (scan)
- `-H, --header` repeatable auth headers
- `-o, --output` output file path
- `--depth`, `--max-pages`, `--timeout`
- `--scope same-origin|same-domain`
- `--headless` (default true)
- `--proxy <url>`
- `--confidence <0-1>`
- `--probe` (enable active probing)
- `--deduplicate`
- `--dangerous-allow-private`
- `-v, --verbose`

## Example set

```bash
vespasian scan https://app.example.com -o api.yaml
vespasian scan https://app.example.com --api-type graphql -o schema.graphql
vespasian crawl https://app.example.com -o capture.json
vespasian import har session.har -o capture.json
vespasian generate rest capture.json -o openapi.yaml
vespasian scan https://app.example.com --proxy http://127.0.0.1:8080 -o api.yaml
```

## Safety note

`--dangerous-allow-private` bypasses SSRF protections and should be used only in authorized local/private testing environments.
