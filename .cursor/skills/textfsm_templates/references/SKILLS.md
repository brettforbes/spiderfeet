# TextFSM NTC Templates References Index

| File | Contents |
|------|----------|
| [parse-api.md](parse-api.md) | `ntc_templates.parse.parse_output`, exceptions, parameters |
| [platform-index.md](platform-index.md) | CliTable index format, Platform/Command attributes, template_dir |
| [extending-templates.md](extending-templates.md) | Add templates, validate, contribute upstream |
| [nugget-conversion.md](nugget-conversion.md) | Parsed dict rows → SpiderFeet nodes/edges from target hierarchy |
| [use-cases-and-workflow.md](use-cases-and-workflow.md) | CLI corpus scenario: text samples + nugget spec → parser function |
| [textfsm-syntax-primer.md](textfsm-syntax-primer.md) | When to drop to raw TextFSM (link to `textfsm` skill) |
| [sources.md](sources.md) | ntc-templates docs, GitHub, blog posts |

**Read order for new agents**

1. `use-cases-and-workflow.md` — understand the `(text, nodes_edges)` input contract.
2. `parse-api.md` — run `parse_output` with platform/command.
3. `platform-index.md` — wire custom OSINT templates into an index.
4. `nugget-conversion.md` — implement `to_nodes_edges()`.
5. `extending-templates.md` — author new `.textfsm` when no template exists.
6. `textfsm-syntax-primer.md` — TextFSM grammar details via sibling skill.

**Sibling skill:** [`../../textfsm/SKILL.md`](../../textfsm/SKILL.md) — raw TextFSM authoring, CliTable internals, pitfalls.

**Operator doc:** [`.docs/docs-for-cli-tools/TextFSM-Templates-Zero-to-Hero.md`](../../../.docs/docs-for-cli-tools/TextFSM-Templates-Zero-to-Hero.md)

**CLI profiling:** [`.cursor/skills/cli_app_profiling/SKILL.md`](../../cli_app_profiling/SKILL.md)
