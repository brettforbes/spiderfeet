# SPEC-006 visual review checklist — Tools Structure + ontology

**Program:** SPEC-006 · **PR:** [#1007](https://github.com/brettforbes/spiderfeet/pull/1007)  
**Operator gate:** [#1006](https://github.com/brettforbes/spiderfeet/issues/1006)

## Preconditions

- `./start.ps1` running (FastAPI + widget)
- CLI Profiling tab open

## Tools → Structure button (all eight)

For each tool, open **Tools** row → **Structure**. Confirm Mermaid renders, section depth matches Nmap bar, no empty pane.

| Tool | Structure doc | VR status | Notes |
|------|---------------|-----------|-------|
| nmap | `nmap_nugget_graph_structure.md` | pending | Gold reference |
| netdiscover | `netdiscover_nugget_graph_structure.md` | pending | |
| nerva | `nerva_nugget_graph_structure.md` | pending | CDN reclassification section |
| pius | `pius_nugget_graph_structure.md` | pending | Org tree |
| subfinder | `subfinder_nugget_graph_structure.md` | pending | Domain apex |
| httpx | `httpx_nugget_graph_structure.md` | pending | URL probe |
| katana | `katana_nugget_graph_structure.md` | pending | **new** |
| nuclei | `nuclei_nugget_graph_structure.md` | pending | **new** |

## Unified ontology

- [ ] Skim `.docs/docs-for-cli-tools/_Current_Ontology.md` — all eight tools in sub-graph table
- [ ] Per-tool sub-graph Mermaid sections present
- [ ] Composition diagram readable

## Sign-off

Operator comment on #1006 with `Validated` or list of fixes needed.
