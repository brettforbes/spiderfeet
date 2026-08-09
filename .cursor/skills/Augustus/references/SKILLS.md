# Augustus References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Command tree, SpiderFeet preferred flags, Captured help pointer |
| [output-and-parsing.md](output-and-parsing.md) | JSON / JSONL attempt schema, harvest bundles |
| [nugget-mapping.md](nugget-mapping.md) | Findings → SpiderFeet `nodes[]` / `edges[]` |
| [tactics.md](tactics.md) | Sequencing, buffs, multi-turn, recon |
| [sources.md](sources.md) | Official repo, blog, releases, docs |

**Read order for new agents**

1. `cli-options.md` — 0.14.15 command tree and SpiderFeet defaults (`--format json`, `-o` JSONL).
2. `output-and-parsing.md` — parse `attempts[]` / JSONL lines into harvest `records[]`.
3. `nugget-mapping.md` — map findings to catalogue nugget ids.
4. `tactics.md` — adapt for smoke, thematic batches, buffs, multi-turn, recon.
5. `sources.md` — upstream docs when help text is insufficient (verify flags against Captured help).

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Augustus-Zero-to-Hero.md` | Install → list → scan → structured → nuggets |
| `.docs/docs-for-cli-tools/Augustus-CLI-Options.md` | Full CLI reference + Captured help (**2026-08-10**) |

**Related skills:** [`../../julius/SKILL.md`](../../julius/SKILL.md) (fingerprint LLM/inference surfaces before Augustus), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md) (HTTP/app templates — different vulnerability class).

**Ontology:** `.docs/analysis/nuggets.json` — prefer `VULNERABILITY_GENERAL`, `RAW_RIR_DATA`, `INTERNET_NAME`, `WEBSERVER_TECHNOLOGY`; do not invent `LLM_*` types without `nuggets_extension.json` approval.
