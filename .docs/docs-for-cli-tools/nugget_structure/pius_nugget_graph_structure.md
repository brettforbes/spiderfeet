# PIUS — proposed nugget graph structure

**Skill:** `.cursor/skills/pius/SKILL.md` · **Epic:** #853 / task #856 · **Keys:** `.docs/docs-for-cli-tools/pius_api_key_mapping.md`

Generator: `.seed/scripts/cli_corpus/cli_tool_to_graph.py` · Binary: `.tools/pius` (WSL)

## Scan head

`SCAN_RECORD` with `SCAN_CLI`, `COMPANY_NAME` (`--org`). Findings attach via `contains`.

## Finding rows (`--output ndjson`)

| PIUS `Type` | Nugget | Relation |
|-------------|--------|----------|
| `domain` | `INTERNET_NAME` | scan `contains` domain; `PIUS_SOURCE` descriptor via `had` |
| `cidr` | `NETBLOCK_OWNER` | scan `contains` netblock; `PIUS_SOURCE` via `had` |
| `preseed` | *(internal)* | Skipped in graph export — pipeline seed only |

## Scenarios examined

| Key | Org / domain | Plugins |
|-----|--------------|---------|
| `passive_bbc_corporate_ndjson` | BBC + bbc.co.uk | crt-sh, gleif, whois, edgar, wikidata, google-dorks |
| `passive_scanme_permissive_ndjson` | Nmap Scanme | crt-sh, gleif, whois |
| `passive_shodan_plugin_ndjson` | Scanme + Shodan key | shodan |
| `cidr_whois_arin_ndjson` | BBC RIR phase | whois, edgar, arin, ripe |
| `passive_obscure_clean_miss_ndjson` | Fictitious org | gleif, whois (sparse) |
| `passive_bbc_terminal_text` | BBC terminal review | crt-sh, gleif |

Filter `needs_review` and company-name false positives in production ingest; retained in examination evidence for semantic coverage.
