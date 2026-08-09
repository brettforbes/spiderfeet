# Julius Match Rules and Custom Probes

Upstream detail: [Match Rules](https://github.com/praetorian-inc/julius/wiki/Match-Rules), [Probe YAML Reference](https://github.com/praetorian-inc/julius/wiki/Probe-YAML-Reference).

## Match rule types

Within a **single request**, rules are combined (AND). Common types from README/wiki:

| Type | Behavior |
|------|----------|
| `status` | HTTP status equals |
| `body.contains` | Case-sensitive substring in body |
| `body.prefix` | Case-sensitive body prefix |
| `header.contains` | Header value contains substring |
| `header.prefix` | Header value prefix |
| `content-type` | Content-Type match |

Types may support **`not: true`** negation (wiki).

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
```

Validate and run (flags from Captured help):

```bash
julius validate ./probes
julius probe -p ./probes -v -o json https://target:9000
```

Empty `path` may be allowed on newer probes (classifies the supplied URL as-is) — see bundled CHANGELOG / wiki before relying on it.

## Model extraction

When a probe defines model extraction (JQ), Julius can populate `models[]` in JSON output. Prefer `-o json` / `-o jsonl` to capture them.

## Architecture notes

- Probes are YAML; binary embeds defaults; `-p` overrides directory.
- Specificity ranks competing matches (higher wins for triage).
- `--augustus` surfaces generator configs when defined on the probe.
