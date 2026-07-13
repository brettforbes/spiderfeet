# SPEC-007 sketch → v1 gap notes

Original sketch: informal `12A` before redesign. Logic master: `12B`. Fixes encoded in `12A` + `12C`.

| Sketch defect | Why it fails | v1 replacement |
|---------------|--------------|----------------|
| `concat({{IP_ADDRESS}}, ":", {{PORT}})` | Global cartesian; no host scope; ignores graph edges | GSE `for_each` + `collect` + `emit.product` |
| `value: {{DOMAIN_NAME}}` / `{{SUBDOMAIN}}` | Template over type name; `SUBDOMAIN` not in ontology | `select.nodes` + `where.related` on `DOMAIN_NAME` / `DOMAIN_NAME_PARENT` |
| `sum({{domains}}, {{subdomains}})` | Informal | `union` binding |
| Broken YAML under `sequence:` (indent) | Not a valid mapping list | `steps:` list of step objects |
| Linear `sequence` only | Cannot express fan-out chains | `needs` DAG |
| `sfp_*` module ids | Adapters are tool names today | `uses: tool.<adapter_id>` |
| Single shell `cli_options` string | Hard for AST / Langium later | `config.argv` string list |
| `temp_file: auto` loose | Unclear input vs output | `files.input` / `files.output` with `mode: auto` |
| `context: graph: {{scan_graph}}` | Unclear merge semantics | `context.export: scan_graph \| none` |
| Targets as full URLs for `-d` | DNS tools want hostnames | `normalize: hostname_from_url` |
| httpx/katana input bugs in sketch | Wrong variable refs (`all_domains` vs `web_url_list`) | Explicit `$steps.<id>.vars.<name>` |

## Ontology corrections agents must respect

- No `SUBDOMAIN` nugget_id in `nuggets.json`
- Port component in nmap graphs is `PORT` (under `TRANSPORT` / via `contains*`), not necessarily `TCP_PORT_OPEN` event name
- Prefer structure docs + corpus graphs over assumed types when writing GSE
