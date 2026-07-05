# httpx References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, PROBES, OUTPUT, MATCHERS, FILTERS, etc. |
| [json-output-schema.md](json-output-schema.md) | `-json` JSON Lines record shapes |
| [probes-matchers-filters.md](probes-matchers-filters.md) | When to enable probes vs matchers vs filters |
| [config-and-ports.md](config-and-ports.md) | `config.yaml`, `-p` ports, `-path`, TLS/CSP probes |
| [workflows-and-phases.md](workflows-and-phases.md) | subfinder → dnsx → httpx → naabu → nuclei |
| [tactics.md](tactics.md) | CDN, redirects, thin yield, rate limits |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet nuggets + `nodes[]`/`edges[]` |
| [sources.md](sources.md) | ProjectDiscovery docs and articles |

**Read order for new agents**

1. `workflows-and-phases.md` — where httpx sits in recon pipelines.
2. `cli-options.md` + `probes-matchers-filters.md` — build probe commands.
3. `json-output-schema.md` — always `-json` for automation.
4. `nugget-mapping.md` — emit web nuggets for corpus and nuclei chaining.
5. `tactics.md` — adapt when CDN-fronted, empty tech-detect, or rate-limited.
6. `config-and-ports.md` — non-default ports and path bruteforce scenarios.

**Operator docs (repo root)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Httpx-Zero-to-Hero.md` | Install → probe → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/Httpx-CLI-Options.md` | Full CLI reference |

**Upstream skills:** [`../../subfinder/SKILL.md`](../../subfinder/SKILL.md), [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md), [`../../naabu/SKILL.md`](../../naabu/SKILL.md)

**Downstream skills:** [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md), [`../../webanalyze/SKILL.md`](../../webanalyze/SKILL.md), [`../../julius/SKILL.md`](../../julius/SKILL.md)

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — httpx extends web/APPLICATIONS layer on qualified `HOST`.
