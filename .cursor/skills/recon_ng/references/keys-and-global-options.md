# Keys and Global Options

## API key management

Many Recon-ng modules require provider credentials. Missing keys commonly cause silent low-yield runs or explicit module failures.

Key workflow:
1. `keys list` to inspect configured providers.
2. `keys add <provider> <value>` for required modules.
3. Validate key-required modules on a minimal SOURCE before full execution.

Operational guidance:
- Keep key usage scoped to authorized engagements.
- Rotate/revoke keys according to provider policy.
- Avoid committing key material into scripts or logs.

## Dependency and key markers

Module metadata typically indicates:
- dependencies (D),
- key requirement (K),
- path/category context.

Treat D/K markers as preflight requirements, not optional hints.

## Global options and execution posture

Global options influence runtime behavior across modules, such as:
- verbosity and debugging visibility,
- request/HTTP behavior (for example user-agent/proxy context where available),
- execution pacing/threading and noise profile,
- output and logging behavior.

Use low-noise defaults for stealth-sensitive workflows and increase verbosity for debugging.

## Rate limit and quota controls

- Run passive/no-key modules first to expand seed set cheaply.
- Defer paid/rate-limited modules until prerequisite tables prove value.
- Use batched SOURCE inputs for provider-heavy modules.
- Track per-module value by row growth and output quality.

## Key-safe automation

When automating with resource scripts or `recon-cli`:
- inject keys from environment/secure runtime stores,
- avoid plaintext key literals in reusable artifacts,
- separate reusable logic scripts from environment-specific secret setup.
