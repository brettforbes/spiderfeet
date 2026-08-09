# Julius References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Captured help (2026-08-10), commands, global + probe flags |
| [json-output-schema.md](json-output-schema.md) | `json` / `jsonl` result fields and parsing rules |
| [probes-and-services.md](probes-and-services.md) | 63 probes from live `julius list`, categories, ports |
| [workflows-and-phases.md](workflows-and-phases.md) | Target intake → probe → adapt → enrich |
| [tactics.md](tactics.md) | Shadow AI discovery, port→URL chaining, hostile nets |
| [nugget-mapping.md](nugget-mapping.md) | JSON results → SpiderFeet nodes and edges |
| [match-rules-and-probes.md](match-rules-and-probes.md) | Probe YAML, match rule types, custom probes |
| [sources.md](sources.md) | GitHub wiki, blog posts, Augustus integration |

**Read order for new agents**

1. `workflows-and-phases.md` — how to run probes and adapt when nothing matches.
2. `cli-options.md` — flags for output, TLS, concurrency, timeouts (Captured help only).
3. `json-output-schema.md` — parse `-o json` / `-o jsonl`.
4. `probes-and-services.md` — which services exist and typical ports.
5. `nugget-mapping.md` — emit SpiderFeet graph JSON.
6. `tactics.md` — chain from Naabu/Nmap; escalate specificity.
7. `match-rules-and-probes.md` — when writing or validating custom probes.

**Operator docs**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Julius-Zero-to-Hero.md` | Install → probe → JSON → nuggets |
| `.docs/docs-for-cli-tools/Julius-CLI-Options.md` | Full CLI reference + Captured help |

**Related skills:** [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../Augustus/SKILL.md`](../../Augustus/SKILL.md)
