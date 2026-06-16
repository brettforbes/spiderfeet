# Vespasian CLI Options

## Main commands

- `vespasian scan <url>`
- `vespasian crawl <url>`
- `vespasian import <burp|har|mitmproxy> <file>`
- `vespasian generate <rest|graphql|wsdl> <capture-file>`

## Shared and high-value flags

- `-o, --output <path>`
- `-H, --header "<k>: <v>"` (repeatable)
- `-v, --verbose`
- `--timeout <duration>`
- `--dangerous-allow-private`

## Scan/crawl flags

- `--depth <n>`
- `--max-pages <n>`
- `--scope same-origin|same-domain`
- `--headless`
- `--proxy <url>`
- `--no-request-id`

## Generation flags

- `--confidence <0-1>`
- `--probe`
- `--deduplicate`

## Examples

```bash
vespasian scan https://app.example.com -o api.yaml
vespasian scan https://app.example.com --api-type graphql -o schema.graphql
vespasian crawl https://app.example.com --depth 5 --max-pages 200 -o capture.json
vespasian import har capture.har -o capture.json
vespasian generate wsdl capture.json -o service.wsdl
vespasian scan https://app.example.com --proxy http://127.0.0.1:8080 -o api.yaml
```

## Notes

- `scan` is convenience mode (`crawl + generate`).
- Use two-stage flow when you need deterministic reruns and artifact reuse.
