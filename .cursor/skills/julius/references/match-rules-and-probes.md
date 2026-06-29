# Julius Match Rules and Custom Probes

## Match rule types (6)

Within a **single request**, all rules are **AND**. See wiki: Match Rules.

| Type | Fields | Behavior |
|------|--------|----------|
| `status` | `value` (int) | HTTP status equals |
| `body.contains` | `value` | Case-sensitive substring in body |
| `body.prefix` | `value` | Case-sensitive body prefix |
| `header.contains` | `header`, `value` | Header value contains substring |
| `header.prefix` | `header`, `value` | Header value prefix |
| `content-type` | `value` | Case-insensitive Content-Type contains |

All types support **`not: true`** negation.

## Request-level strategies

| `require` | Meaning |
|-----------|---------|
| `any` | Stop at first matching request in probe |
| `all` | Every request in probe must match |

## Minimal probe YAML skeleton

```yaml
name: my-custom-llm
description: Detect internal custom API
category: self-hosted
port_hint: 9000
specificity: 70
require: any
requests:
  - path: /v1/models
    method: GET
    match:
      - type: status
        value: 200
      - type: content-type
        value: application/json
      - type: body.contains
        value: '"object":"list"'
models:
  jq: '.data[].id'   # see Probe YAML Reference for exact schema
```

Validate:

```bash
julius validate ./probes
julius probe -p ./probes -v -o json https://target:9000
```

## Model extraction

When probe defines `models` with JQ expression, Julius performs an extra HTTP request and evaluates with **gojq**. Extracted names appear in `models[]` JSON field.

## Architecture notes

- Probes embedded at compile time (`//go:embed probes/*.yaml`).
- `--probes-dir` overrides for development.
- Response cache: MD5 key + singleflight deduplication.
- Results sorted by **specificity descending**.

Full probe schema: https://github.com/praetorian-inc/julius/wiki/Probe-YAML-Reference

## Adding new rule types (upstream)

Contributors implement `Rule` interface in `pkg/rules/` and register via `init()`. Not required for SpiderFeet operators — use YAML probes only.
