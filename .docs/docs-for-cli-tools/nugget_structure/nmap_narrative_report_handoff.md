# Nmap Narrative Report — Operator Handoff

**Epic:** GitHub #844 · **Spec:** `.seed/05_Onotology_for_Nuggets.md` §4.3 · **Program plan:** `.seed/planning/NARRATIVE_REPORT_PROGRAM.md`

## What changed

CLI profiling **Graph description** artifacts (`*_proposed_nuggets_edges_description.md`) are now **template-driven OSINT narratives**, not statistics summaries. Every `nugget_data` value from the semantic graph appears in the story or the appendix.

## Gold-standard sample

Read the capstone permissive narrative first — it exercises the maximum Nmap story (scan, host environment/networks/applications, SSH keys, traceroute, Mermaid diagram, appendix):

- **Narrative:** [nmap_capstone_permissive_proposed_nuggets_edges_description.md](./nmap_capstone_permissive_proposed_nuggets_edges_description.md)
- **Graph JSON:** [nmap_capstone_permissive_proposed_nuggets_edges.json](./nmap_capstone_permissive_proposed_nuggets_edges.json)
- **Structure reference:** [nmap_nugget_graph_structure.md](./nmap_nugget_graph_structure.md)

Sparse scenarios (host discovery only, Windows enrich local, etc.) use the **same report shape** with empty subsections omitted or noted as “no transport endpoints enumerated.”

## Engine

| Component | Path |
|-----------|------|
| Generic builder | `.seed/scripts/cli_corpus/narrative_report.py` |
| Nmap integration | `nmap_xml_to_graph.describe_graph()` → `build_nmap_narrative_report()` |
| Regenerate all scenarios | `python .seed/scripts/cli_corpus/nmap_xml_to_graph.py --all` |

### Report structure (maximum story)

1. Title and introduction  
2. **Scan** — tool, version, target, CLI, timing, host count  
3. **Each host** — entity, environment (OS), networks (IP → ports), applications (services, CPE, SSH keys), vulnerabilities (when present)  
4. **Trace** — hop list + Mermaid `flowchart LR` (when trace nuggets exist)  
5. Conclusion  
6. Appendix — tabular inventory of every nugget  
7. Footer — `OS-Intel Scan` with scan date  

Traversal uses ontology relations: `contains` / `had` for hierarchy, `listens-to` for port ↔ service peers.

## Verification

```bash
pytest .tests/test_narrative_report.py .tests/test_nmap_xml_to_graph.py -q
```

Coverage check (every node value in output):

```python
from narrative_report import build_nmap_narrative_report, validate_narrative_coverage
ok, missing = validate_narrative_coverage(graph, markdown)
```

All **15** Nmap scenario graphs pass coverage validation after regeneration.

## Widget review

After merge, restart the widget (port 4001) and open **CLI Profiling → Nmap → capstone_permissive → Graph description**. Mermaid trace diagrams render via the widget markdown pipeline.
