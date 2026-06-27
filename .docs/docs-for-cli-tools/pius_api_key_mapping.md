# PIUS API key mapping (Subscriptions → harvest env)

Pius plugins read **environment variables**. SpiderFeet **Subscriptions** tab stores keys on matching `sfp_*` modules. Run:

```bash
poetry run python .seed/scripts/cli_corpus/sync_pius_env.py
```

This writes gitignored `.tools/pius.env` consumed by `harvest.py` for `pius` scenarios.

## Module → PIUS env

| Subscriptions module | PIUS env var | Plugin(s) |
|---------------------|--------------|-----------|
| `sfp_shodan` | `SHODAN_API_KEY` | shodan, favicon-hash |
| `sfp_securitytrails` | `SECURITYTRAILS_API_KEY` | passive-dns |
| `sfp_censys` | `CENSYS_API_TOKEN`, `CENSYS_ORG_ID` | censys-org |
| `sfp_builtwith` | `BUILTWITH_API_KEY` | builtwith |
| `sfp_whoxy` | `WHOXY_API_KEY` | whoxy-reverse-whois |
| `sfp_binaryedge` | `BINARYEDGE_API_KEY` | (future) |
| `sfp_github` | `GITHUB_TOKEN` | github-org |

## No SpiderFeet module (manual / future accordion)

| PIUS env | Plugin | Signup notes |
|----------|--------|--------------|
| `APOLLO_API_KEY` | apollo | apollo.io API |
| `VIEWDNS_API_KEY` | reverse-whois, reverse-ip | viewdns.info |
| `FOFA_API_KEY` | favicon-hash | fofa.info |

Plugins without keys self-disable; passive scenarios (`crt-sh`, `gleif`, `whois`, `edgar`, `wikidata`) run without credentials.

## Binary

Linux binary: `.tools/pius` (v1.0.16). Harvest invokes via `/mnt/c/projects/spiderfeet/.tools/pius`.
