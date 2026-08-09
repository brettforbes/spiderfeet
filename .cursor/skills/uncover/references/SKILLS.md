# uncover References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, SEARCH-ENGINE, CONFIG, OUTPUT, DEBUG |
| [output-and-parsing.md](output-and-parsing.md) | `-json` JSONL record shape and parse notes |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet nuggets + `nodes[]`/`edges[]` |
| [tactics.md](tactics.md) | Query narrowing, multi-engine, IP/CIDR, pipelines |
| [sources.md](sources.md) | Official docs, provider config, articles |

**Read order for new agents**

1. `cli-options.md` — build commands from live flag set (**v1.2.1**, **2026-08-10**).
2. `output-and-parsing.md` — always `-json` for automation.
3. `nugget-mapping.md` — emit address/port/name nuggets.
4. `tactics.md` — adapt when keys fail, yield is thin, or noise is high.
5. `sources.md` — upstream README and provider setup.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/uncover-Zero-to-Hero.md` | Install → keys → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/uncover-CLI-Options.md` | Full CLI reference + captured help |

**Help captures:** `.tmp_uncover_help/` — **2026-08-10**, binary `C:\projects\spiderfeet\.tools\uncover\uncover.exe` **v1.2.1**.

**Upstream / peer skills:** [`../../naabu/SKILL.md`](../../naabu/SKILL.md) (passive InternetDB overlap), [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md), [`../../subfinder/SKILL.md`](../../subfinder/SKILL.md)

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — uncover feeds NETWORKS (hosts/IPs/ports) before APPLICATIONS probing.
