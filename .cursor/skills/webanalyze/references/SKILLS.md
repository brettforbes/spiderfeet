# webanalyze References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Captured help (2026-08-10), all flags, invocation notes |
| [output-schema-and-parsing.md](output-schema-and-parsing.md) | `-output json` NDJSON shape, CSV/stdout, stderr errors |
| [nugget-mapping.md](nugget-mapping.md) | Matches → SpiderFeet `INTERNET_NAME` / `WEBSERVER_TECHNOLOGY` |
| [tactics-and-workflows.md](tactics-and-workflows.md) | Breadth/depth fingerprinting and category pivots |
| [sources.md](sources.md) | Official repo, fingerprint ecosystem, guides |

**Read order for new agents**

1. `cli-options.md` — flags from live `-h` only (`-output json`, not invented `-json`).
2. `output-schema-and-parsing.md` — parse JSON lines for corpus.
3. `nugget-mapping.md` — emit SpiderFeet graph JSON.
4. `tactics-and-workflows.md` — when to crawl, redirect, or batch.
5. `sources.md` — upstream docs and definition sources.

**Operator docs**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/webanalyze-Zero-to-Hero.md` | Install → update → JSON → nuggets |
| `.docs/docs-for-cli-tools/webanalyze-CLI-Options.md` | Full CLI reference + Captured help |

**Related skills:** [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../cmseek/SKILL.md`](../../cmseek/SKILL.md), [`../../wafwoof/SKILL.md`](../../wafwoof/SKILL.md), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md)
