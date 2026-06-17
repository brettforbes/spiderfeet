# PIUS CLI Options

## Install

```bash
go install github.com/praetorian-inc/pius/cmd/pius@latest
```

Requires Go 1.25.0+. Binary typically at `~/go/bin/pius`.

## Commands

| Command | Description |
|---------|-------------|
| `pius run` | Execute discovery pipeline |
| `pius list` | List registered plugins |

## `pius run` flags

| Short | Long | Default | Description |
|-------|------|---------|-------------|
| `-o` | `--org` | *(required)* | Organization name to search |
| `-d` | `--domain` | — | Known domain hint (unlocks crt-sh, passive-dns, DNS plugins) |
| | `--asn` | — | ASN hint, e.g. `AS12345` (unlocks `asn-bgp`) |
| | `--plugins` | all | Comma-separated plugin whitelist |
| | `--disable` | — | Comma-separated plugin blacklist |
| | `--concurrency` | `5` | Max concurrent plugins |
| `-f` | `--output` | `terminal` | `terminal`, `json`, or `ndjson` |
| | `--mode` | `passive` | `passive`, `active`, or `all` |
| | `--doh-wordlist` | — | Wordlist path for `doh-enum` plugin |
| | `--doh-servers` | — | Comma-separated DoH resolver URLs |
| | `--doh-gateways` | — | Comma-separated AWS API Gateway URLs for DoH |
| | `--doh-deploy-gateways` | — | Auto-deploy AWS API Gateways for IP rotation |

### SpiderFeet / pipeline default

```bash
pius run --org "ORG NAME" --domain example.com --output ndjson
```

## Mode matrix

| Mode | Passive plugins | Active plugins (`dns-brute`, `dns-zone-transfer`, `doh-enum`, `favicon-hash`, …) |
|------|-----------------|----------------------------------------------------------------------------------|
| `passive` | Yes | No |
| `active` | No | Yes |
| `all` | Yes | Yes |

Plugins with missing API keys self-disable via `Accepts()` — no error, simply skipped.

## Environment variables

| Variable | Plugin(s) | Required |
|----------|-----------|----------|
| `APOLLO_API_KEY` | `apollo` | Yes |
| `GITHUB_TOKEN` | `github-org` | No (raises rate limit) |
| `SECURITYTRAILS_API_KEY` | `passive-dns` | Yes |
| `VIEWDNS_API_KEY` | `reverse-whois`, `reverse-ip` | Yes / optional |
| `WHOXY_API_KEY` | `whoxy-reverse-whois` | Yes |
| `BUILTWITH_API_KEY` | `builtwith` | Yes |
| `SHODAN_API_KEY` | `shodan`, `favicon-hash` | Yes |
| `FOFA_API_KEY` | `favicon-hash` | No |
| `CENSYS_API_TOKEN` | `censys-org` | Yes |
| `CENSYS_ORG_ID` | `censys-org` | Yes |
| AWS credentials | `doh-enum` with `--doh-deploy-gateways` | When deploying gateways |

## Cache

Location: `~/.pius/cache/`

| Type | TTL | Used by |
|------|-----|---------|
| API JSON cache | 24h | apollo, github-org, censys-org, … |
| RPSL gzip cache | 24h | apnic, afrinic |

Clear: `rm -rf ~/.pius/cache/`

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Runtime error |

## Examples

```bash
# Passive NDJSON pipeline
pius run --org "Acme Corp" --domain acme.com --output ndjson

# CIDR-only plugin set
pius run --org "Acme Corp" --plugins whois,arin,ripe --output ndjson

# Active DNS brute (authorized)
pius run --org "Acme Corp" --domain acme.com --mode active --plugins dns-brute --output ndjson

# Terminal review
pius run --org "Acme Corp" --domain acme.com

# JSON array file
pius run --org "Acme Corp" --output json > out.json
```

## `pius list`

Prints registered plugins with name, category, phase, and mode. Use to build `--plugins` / `--disable` lists.
