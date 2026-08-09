# tldfinder References Index

Evidence binary: `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe`  
Version: **v0.0.2** (captured **2026-08-10**)  
Help capture: `.tmp_tldfinder_help/`

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Flags grouped by INPUT, SOURCE, FILTER, OUTPUT, CONFIGURATION, etc. |
| [output-schema-and-parsing.md](output-schema-and-parsing.md) | `-oJ` JSONL record shapes (`host`, `input`, `source`/`sources`, `ip`) |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet `INTERNET_NAME`, IP nodes, edges |
| [tactics-and-workflows.md](tactics-and-workflows.md) | Private-TLD discovery sequencing and adaptation |
| [sources.md](sources.md) | Official docs, releases, and practitioner links |

**Read order for new agents**

1. `tactics-and-workflows.md` — when to use dns/tld/domain modes and how to chain dnsx.
2. `cli-options.md` — exact flags from the installed binary (do not invent switches).
3. `output-schema-and-parsing.md` — parse `-oJ` / `-cs` / `-oI` variants.
4. `nugget-mapping.md` — emit graph nodes and edges for corpus.
5. `sources.md` — upstream docs and research context.

**Operator docs**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/tldfinder-Zero-to-Hero.md` | Install → discover → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/tldfinder-CLI-Options.md` | Full CLI help reference (v0.0.2) |

**Downstream skills:** [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md), [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../subfinder/SKILL.md`](../../subfinder/SKILL.md).
