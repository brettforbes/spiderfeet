# Subfinder References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, SOURCE, FILTER, OUTPUT, CONFIGURATION, etc. |
| [json-output-schema.md](json-output-schema.md) | `-oJ` JSON Lines record shapes |
| [provider-config.md](provider-config.md) | `provider-config.yaml`, API keys, `-ls` sources |
| [workflows-and-phases.md](workflows-and-phases.md) | Passive → validate → scan pipelines |
| [tactics.md](tactics.md) | Thin results, rate limits, defensive targets |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet `INTERNET_NAME`, `IP_ADDRESS` |
| [sources.md](sources.md) | ProjectDiscovery docs, GitHub, articles |

**Read order for new agents**

1. `workflows-and-phases.md` — when to use passive vs active, piping to dnsx/httpx/naabu.
2. `provider-config.md` — configure keys before blaming the tool for empty output.
3. `cli-options.md` — flags for domains, sources, JSONL, filters.
4. `json-output-schema.md` — parse `-oJ` / `-cs` / `-oI` variants.
5. `nugget-mapping.md` — emit graph nodes and edges for corpus.
6. `tactics.md` — adapt when enumeration is blocked or noisy.

**Operator docs (repo root)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/SubFinder-Zero-to-Hero.md` | Install → enumerate → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/SubFinder-CLI-Options.md` | Full CLI reference |

**Downstream skills:** [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md), [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md) — chain with ProjectDiscovery **httpx** after subdomain validation.
