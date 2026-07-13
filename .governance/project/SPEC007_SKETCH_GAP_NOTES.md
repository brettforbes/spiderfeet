# SPEC-007 sketch → v1 gap notes

**Issue:** [#1015](https://github.com/brettforbes/spiderfeet/issues/1015) · **Epic P:** [#1009](https://github.com/brettforbes/spiderfeet/issues/1009)  
**Logic master:** `.seed/12B_Workflow_DSL_Description.md`  
**v1 example:** `.seed/12A_Workflow_YAML_Example.yaml`  
**GSE normative:** `.seed/12C_Graph_Select_Language.md`

This document inventories every defect in the **pre-v1 workflow sketch** and records how v1 fixes it. Reviewers and lesser agents should read this before changing schemas or GSE semantics.

---

## 1. Global sketch defects (language / structure)

| Sketch defect | Why it fails | v1 replacement | Verified in |
|---------------|--------------|----------------|-------------|
| `concat({{IP_ADDRESS}}, ":", {{PORT}})` | Global cartesian; no host scope; ignores `contains` edges | GSE `for_each` + `collect` + `emit.product` + `join` | 12A `nmap_ports.output.vars.ip_port_list`; 12C §5 |
| `value: {{DOMAIN_NAME}}` / `{{SUBDOMAIN}}` | Template over type name; not graph traversal | GSE `select.nodes` + `where.related` | 12A `subfinder_enum` vars |
| `{{SUBDOMAIN}}` nugget id | **Not in ontology** (`nuggets.json`) | `DOMAIN_NAME` + `DOMAIN_NAME_PARENT` predicate | 12C §4.1; subfinder corpus |
| `sum({{domains}}, {{subdomains}})` | Informal function | GSE `union` binding | 12A `all_domains` |
| `sequence:` with broken YAML indent | Invalid mapping (`- sfp_subfinder:` child keys mis-indented) | `steps:` list of step objects | 12A structure |
| Linear `sequence` only | Cannot express fan-out (ports chain vs web chain) | `needs` DAG | 12A `nmap_ports` + `httpx_live` both need `subfinder_enum` |
| `sfp_*` module ids in `info.modules` / step keys | Adapters are `tool.<id>` today; no workflow-aware `sfp_*` yet | `uses: tool.subfinder` etc. | 12B §4.4 |
| Single shell `cli_options` string | Hard for Langium AST; escaping/splitting fragile | `config.argv` string list | 12A each step |
| `temp_file: auto` (undifferentiated) | Unclear input vs output file roles | `files.input` / `files.output` with `mode: auto` | 12A `config.files` |
| `context: graph: {{scan_graph}}` | Unclear merge semantics | `context.export: scan_graph \| none` | 12B §2.5; 12A interim steps |
| `targets: https://…` passed to `-d` | DNS tools expect hostname | `normalize: hostname_from_url` on step input | 12A `subfinder_enum.input` |
| `{{scan_graph}}` in output | Graph is step artifact, not a template var | `$step.scan_graph` as GSE `source` only | 12C §7 |

---

## 2. Per-step sketch logic vs v1 (attack-surface example)

Original intent from 12B §3.3–3.5. Sketch step names used `sfp_*`; v1 uses stable step `id` + `uses: tool.*`.

| Sketch step | Sketch input (as written) | Sketch output (as written) | Sketch bugs | v1 step id | v1 fix |
|-------------|---------------------------|----------------------------|-------------|------------|--------|
| `sfp_subfinder` | `{{targets}}` | `domains`, `subdomains`, `all_domains` via `{{DOMAIN_NAME}}` / `{{SUBDOMAIN}}` / `sum` | SUBDOMAIN type; no parent/apex split | `subfinder_enum` | GSE apex vs child `DOMAIN_NAME`; `union` for `all_domains` |
| `sfp_nmap` | `{{all_domains}}` (sketch said `subdomains` in prose §3.4 inconsistency) | `ip_port_list` via `concat(IP, PORT)` | No host scope; wrong input in prose | `nmap_ports` | `from: $steps.subfinder_enum.vars.all_domains`; GSE `for_each` product |
| `sfp_nerva` | `{{ip_port_list}}` (prose wrongly said `subdomains`) | none | Prose/config copy-paste from nmap | `nerva_services` | Correct input ref; context export only |
| `sfp_httpx` | `{{all_domains}}` | `web_url_list` via `{{URL_WEB_FRAMEWORK}}` | Type name not in all httpx graphs; no filter | `httpx_live` | GSE under HOST with `HTTP_STATUS_CODE`; interim `export: none` |
| `sfp_katana` | sketch used `{{all_domains}}` in YAML but prose said `web_url_list` | `internal_url_list` via `{{LINKED_URL_INTERNAL}}` | **Wrong input in YAML** | `katana_crawl` | `from: $steps.httpx_live.vars.live_hosts` |
| `sfp_nuclei` | sketch used `{{all_domains}}` | context only | **Wrong input** — should be crawl URLs | `nuclei_vulns` | `from: $steps.katana_crawl.vars.crawl_urls` |

---

## 3. Ontology corrections agents must respect

| Assumption in sketch | Reality in corpus graphs | Action |
|----------------------|--------------------------|--------|
| `SUBDOMAIN` nugget | Subfinder emits `DOMAIN_NAME` + optional `DOMAIN_NAME_PARENT` | Use GSE `where.related` / `not.related` |
| `PORT` vs `TCP_PORT_OPEN` | Nmap graphs use `PORT` under `TRANSPORT` / `contains*` | GSE `nugget_id: PORT` with transitive contains from endpoint |
| `URL_WEB_FRAMEWORK` for httpx URLs | httpx graphs use `DOMAIN_NAME`, `HOST`, `HTTP_*` under host tree | Derive `live_hosts` from probe tree; confirm ids in httpx structure doc |
| `LINKED_URL_INTERNAL` for katana | Katana corpus may be sparse; may include `DOMAIN_NAME` only | 12A lists `LINKED_URL_*` + `DOMAIN_NAME` fallback; tighten when corpus proves ids |

**Rule:** Before locking GSE for a tool, read `nugget_structure/<tool>_nugget_graph_structure.md` and a `*_proposed_nuggets_edges.json` fixture.

---

## 4. Archived original sketch excerpt (pre-v1, invalid)

Preserved for diff review only — **do not copy into workflows**.

```yaml
# INVALID — pre-v1 sketch (truncated)
sequence:
  - sfp_subfinder:
    output:
      - domains:
        - type: list
          value: {{DOMAIN_NAME}}
      - all_domains:
        - type: list
          value: sum({{domains}}, {{subdomains}})
  - sfp_nmap:
    output:
        - ip_port_list:
          - type: list
            value: concat({{IP_ADDRESS}}, ":", {{PORT}})
  - sfp_katana:
    input:
      - type: list
        value: {{all_domains}}          # bug: should be web_url_list
  - sfp_nuclei:
    input:
      - type: list
        value: {{all_domains}}          # bug: should be internal_url_list
```

---

## 5. Cross-link checklist (P0)

| Artifact | Links to gap notes |
|----------|-------------------|
| 12B companion table | Yes — see 12B header |
| 12B §7 | Points here for full inventory |
| 12C | References ontology fixes §3 |
| SPEC007_AGENT_PLAN P0 | Done when this file complete |
| AGENTS.md | Via SPEC-007 row → 12B/12C |

---

## 6. Verification (P0 acceptance)

Manual:

- [ ] Table §1 includes: `concat`, `SUBDOMAIN`, `sum`, `sequence`, `sfp_*`, shell `cli_options`
- [ ] Table §2 covers all six sketch steps
- [ ] 12B companion docs link to this file

Automated:

```bash
poetry run pytest .tests/test_spec007_sketch_gap_notes.py -q
```
