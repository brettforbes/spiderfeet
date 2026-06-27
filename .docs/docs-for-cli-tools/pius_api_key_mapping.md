# PIUS API key mapping (Subscriptions → harvest env)

All Pius environment variables are managed through the **Subscriptions** tab. Saving a key automatically updates `.tools/pius.env` when Pius is registered under **Settings → CLI App Paths**.

Optional manual sync:

```bash
poetry run python .seed/scripts/cli_corpus/sync_pius_env.py
```

See `.docs/analysis/centralized_credential_management.md` and `.docs/analysis/credential_registry.json`.

## Module / provider → PIUS env

| Subscriptions provider | PIUS env var | Plugin(s) |
|------------------------|--------------|-----------|
| `sfp_shodan` | `SHODAN_API_KEY` | shodan, favicon-hash |
| `sfp_securitytrails` | `SECURITYTRAILS_API_KEY` | passive-dns |
| `sfp_censys` (UID + Secret fields) | `CENSYS_ORG_ID`, `CENSYS_API_TOKEN` | censys-org |
| `sfp_builtwith` | `BUILTWITH_API_KEY` | builtwith |
| `sfp_whoxy` | `WHOXY_API_KEY` | whoxy-reverse-whois |
| `sfp_binaryedge` | `BINARYEDGE_API_KEY` | (future) |
| `cli_pius_apollo` | `APOLLO_API_KEY` | apollo |
| `cli_pius_viewdns` | `VIEWDNS_API_KEY` | reverse-whois, reverse-ip |
| `cli_pius_fofa` | `FOFA_API_KEY` | favicon-hash |
| `cli_pius_github` | `GITHUB_TOKEN` | github-org |

Plugins without keys self-disable; passive scenarios (`crt-sh`, `gleif`, `whois`, `edgar`, `wikidata`) run without credentials.

## Binary

Linux binary: `.tools/pius` (v1.0.16). Harvest invokes via `/mnt/c/projects/spiderfeet/.tools/pius`.
