# Centralized Credential Management

**Epic:** GitHub #858 · **Registry:** `.docs/analysis/credential_registry.json`

## Overview

SpiderFeet now centralizes third-party API keys and subscription credentials:

| Surface | Purpose |
|---------|---------|
| **Subscriptions** tab | All SpiderFeet OSINT module keys **and** CLI-only keys (Pius Apollo, ViewDNS, FoFA, GitHub token) |
| **Settings** tab (gear icon) | CLI app binary paths + AI agent API keys |
| **Backend vault** | Fernet encryption at rest for module secrets in SQLite |
| **CLI sync engine** | On subscription save, rewrites registered CLI env files (e.g. `.tools/pius.env`) |

## Save flow

1. Operator saves key in **Subscriptions** accordion.
2. Backend encrypts secret → persists → calls `sync_cli_apps_for_provider()`.
3. Registered CLI apps with `env_file` paths receive updated variables.

Manual sync still available:

```bash
poetry run python .seed/scripts/cli_corpus/sync_pius_env.py
```

## Security

- API responses mask secrets (`••••••` + last 4 chars only).
- Module opts stored as `enc:v1:…` in `tbl_config`.
- CLI-only keys in encrypted `{dataPath}/settings/cli_credentials.json`.
- AI agent keys in encrypted `{dataPath}/settings/ai_agents.json`.
- Master key: `{dataPath}/.spiderfeet_credential.key` (or `SPIDERFEET_CREDENTIAL_KEY` env).

Red-team tests: `.tests/credentials/test_security.py`, `.tests/api/test_subscriptions.py`.

## Extending for new CLI tools

1. Add entry under `cli_apps` in `credential_registry.json`.
2. Add `providers` with `env_mappings` for each env var.
3. Register default path in Settings → CLI App Paths.
4. Subscriptions accordions appear automatically for `cli_only` providers.
