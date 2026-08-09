# dnsx References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, QUERY, FILTER, OUTPUT, etc. |
| [json-output-schema.md](json-output-schema.md) | `-json` JSON Lines record shapes |
| [workflows-and-phases.md](workflows-and-phases.md) | subfinder → dnsx → httpx → naabu → nuclei |
| [tactics.md](tactics.md) | Wildcards, resolvers, thin yield, rate limits |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet nuggets + `nodes[]`/`edges[]` |
| [sources.md](sources.md) | ProjectDiscovery docs and articles |

**Read order for new agents**

1. `workflows-and-phases.md` — where dnsx sits in recon pipelines.
2. `cli-options.md` — build query commands from live flag set.
3. `json-output-schema.md` — always `-json` for automation.
4. `nugget-mapping.md` — emit DNS/host nuggets for corpus and httpx chaining.
5. `tactics.md` — adapt when wildcards, SERVFAIL, or thin answers appear.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/dnsx-Zero-to-Hero.md` | Install → resolve → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/dnsx-CLI-Options.md` | Full CLI reference + captured help |

**Help captures:** `.tmp_dnsx_help/` — **2026-08-10**, binary `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe` **v1.2.3**.

**Upstream skills:** [`../../subfinder/SKILL.md`](../../subfinder/SKILL.md)

**Downstream skills:** [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md)

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — dnsx feeds NETWORKS / host qualification before APPLICATIONS.
