# Julius References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Commands (`probe`, `list`, `validate`) and all global flags |
| [json-output-schema.md](json-output-schema.md) | `json` / `jsonl` result fields and parsing rules |
| [probes-and-services.md](probes-and-services.md) | 32 supported LLM platforms by category, port hints, specificity |
| [workflows-and-phases.md](workflows-and-phases.md) | Target intake → probe → adapt → enrich pipelines |
| [tactics.md](tactics.md) | Shadow AI discovery, port→URL chaining, hostile/filtered networks |
| [nugget-mapping.md](nugget-mapping.md) | JSON results → SpiderFeet nodes and edges |
| [match-rules-and-probes.md](match-rules-and-probes.md) | Probe YAML, match rule types, custom probes |
| [sources.md](sources.md) | GitHub wiki, blog posts, Augustus integration |

**Read order for new agents**

1. `workflows-and-phases.md` — how to run probes and adapt when nothing matches.
2. `cli-options.md` — flags for output, concurrency, timeouts.
3. `json-output-schema.md` — parse `-o jsonl` for automation.
4. `probes-and-services.md` — know which services exist and typical ports.
5. `nugget-mapping.md` — emit SpiderFeet graph JSON.
6. `tactics.md` — chain from Naabu/Nmap; escalate specificity.
7. `match-rules-and-probes.md` — when writing or validating custom probes.

**Operator docs (repo root)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Julius-Zero-to-Hero.md` | Install → probe → JSON → nuggets |
| `.docs/docs-for-cli-tools/Julius-CLI-Options.md` | Full CLI reference |

**Related skills:** [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../Augustus/SKILL.md`](../../Augustus/SKILL.md)
