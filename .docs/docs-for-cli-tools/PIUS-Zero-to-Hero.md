# PIUS Zero to Hero — Organizational Attack Surface Discovery

Guide from install through NDJSON pipelines and SpiderFeet nugget mapping.

## 0. What Pius does

**Pius** maps an organization's external attack surface from a **company name**:

- **Domains** — certificate transparency, passive DNS, reverse WHOIS, GitHub, GLEIF, …
- **CIDRs** — all five RIRs (ARIN, RIPE, APNIC, AFRINIC, LACNIC) via handle discovery and resolution

26 plugins, three-phase pipeline, confidence scoring, passive-by-default.

## 1. Install

```bash
go install github.com/praetorian-inc/pius/cmd/pius@latest
pius list
```

Requires Go 1.25+. Ensure `~/go/bin` is on PATH.

## 2. First run

```bash
pius run --org "Acme Corp" --domain acme.com
```

Terminal output:

```
[domain] api.acme.com (crt-sh)
[cidr] 203.0.113.0/24 (arin)
```

## 3. NDJSON for pipelines

```bash
pius run --org "Acme Corp" --domain acme.com --output ndjson
```

One JSON object per line:

```json
{"Type":"domain","Value":"api.acme.com","Source":"crt-sh","Data":null}
{"Type":"cidr","Value":"203.0.113.0/24","Source":"arin","Data":null}
```

SpiderFeet / automation should use **`--output ndjson`**.

## 4. Essential flags

| Flag | Purpose |
|------|---------|
| `--org` | Organization name (required) |
| `--domain` | Unlocks CT and DNS plugins |
| `--asn` | BGP prefix discovery |
| `--mode passive\|active\|all` | Control intrusive plugins |
| `--plugins` / `--disable` | Plugin whitelist/blacklist |
| `--output ndjson` | Stream parseable output |
| `--concurrency N` | Parallelism (default 5) |

Full reference: `.docs/docs-for-cli-tools/PIUS-CLI-Options.md`

## 5. API keys (optional)

Plugins without keys are skipped silently:

```bash
export SECURITYTRAILS_API_KEY="..."
export VIEWDNS_API_KEY="..."
export GITHUB_TOKEN="..."
pius run --org "Acme Corp" --domain acme.com --output ndjson
```

See `.cursor/skills/pius/references/cli-options.md` for full env var table.

## 6. Three-phase pipeline (summary)

1. **Phase 0** — concurrent domain/CIDR plugins (crt-sh, asn-bgp, …)
2. **Phase 1** — `whois` + `edgar` discover RIR handles
3. **Phase 2** — `arin`, `ripe`, `apnic`, `afrinic`, `lacnic` resolve CIDRs
4. **Late stage** — `dns-permutation`, `reverse-ip`, `builtwith` consume discovered assets

Detail: `.cursor/skills/pius/references/plugins-and-phases.md`

## 7. Filter with jq

```bash
# Domains only
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -r 'select(.Type=="domain") | .Value'

# CIDRs only
pius run --org "Acme" --output ndjson \
  | jq -r 'select(.Type=="cidr") | .Value'

# Skip review queue
pius run --org "Acme" --output ndjson \
  | jq 'select(.Data.needs_review != true)'
```

## 8. Map to SpiderFeet nuggets

| PIUS | SpiderFeet |
|------|------------|
| `Type: domain` | `INTERNET_NAME` |
| `Type: cidr` | `NETBLOCK_OWNER` |

See `.cursor/skills/pius/references/nugget-mapping.md`

## 9. Downstream toolchain

```
PIUS (--output ndjson)
    ├─ domains → WAFWOOF → CMSeeK → Nuclei
    └─ cidrs   → Nmap / naabu → Nerva
```

## 10. Troubleshooting

| Problem | Fix |
|---------|-----|
| No domains | Add `--domain` |
| No CIDRs | Try org name variants; run `--plugins whois` alone |
| Stale APNIC | `rm -rf ~/.pius/cache/` |
| GitHub rate limit | `export GITHUB_TOKEN=...` |
| Too slow | `--concurrency 2` or narrower `--plugins` |

## 11. Safety

Passive mode still queries OSINT APIs. Active mode (`dns-brute`, `dns-zone-transfer`, `doh-enum`) sends DNS traffic to targets. Authorized use only.

## 12. Skill reference

`.cursor/skills/pius/SKILL.md`
