# Keys and Global Options

## API keys

Many marketplace modules require provider credentials (metadata **K** markers). Missing keys cause failures or empty yield.

Console workflow:

```text
keys list
keys add <provider> <value>
```

Guidance:

- Scope keys to authorized engagements
- Smoke-test K modules on tiny SOURCE before full scope
- Never commit key literals into resource scripts or git
- For automation, inject from secure environment / secret store

## Dependency markers

Module info typically indicates:

- **D** — software/library dependencies
- **K** — API key requirements

Treat both as preflight gates.

## Captured global options (5.1.2)

From `recon-cli --stealth -G` on **2026-08-10** (marketplace/version checks disabled in that capture):

| Name | Default (capture) | Required | Description |
|------|-------------------|----------|-------------|
| NAMESERVER | 8.8.8.8 | yes | default nameserver for the resolver mixin |
| PROXY | *(empty)* | no | proxy server (address:port) |
| THREADS | 10 | yes | number of threads (where applicable) |
| TIMEOUT | 10 | yes | socket timeout (seconds) |
| USER-AGENT | Recon-ng/v5 | yes | user-agent string |
| VERBOSITY | 1 | yes | 0 = minimal, 1 = verbose, 2 = debug |

Set via `recon-cli -g name=value` (repeatable) or interactive global options commands.

## Rate limits and quotas

- Passive / no-key modules first
- Defer paid modules until prerequisite tables prove value
- Batch SOURCE for provider-heavy modules
- Measure value by row growth and quality, not wall-clock alone

## Stealth vs keys

`--stealth` disables framework passive requests (`--no-version --no-analytics --no-marketplace`). It does **not** replace careful USER-AGENT/PROXY/THREADS tuning for module traffic. Install modules before relying on stealth mode.
