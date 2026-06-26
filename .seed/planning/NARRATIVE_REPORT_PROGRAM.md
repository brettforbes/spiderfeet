# Narrative Report Program (Ontology §4.3)

**Spec:** `.seed/05_Onotology_for_Nuggets.md` §4 Document Generation  
**Requirement:** SPEC_GAP → R2-04-09 (narrative scenario reports from semantic graphs)

## Goal

Convert any CLI app's `nodes` + `edges` semantic graph into a readable Markdown OSINT narrative where **every nugget and value** appears in prose or the appendix. Subsets of the maximum graph produce the same report shape with fewer sections filled.

## Architecture

| Layer | Module | Role |
|-------|--------|------|
| Index | `.seed/scripts/cli_corpus/narrative_report.py` → `SemanticGraph` | Walk `had` / `contains` / `listens-to` |
| Template | `NarrativeReportBuilder` | Section templates per §4.3 order |
| Tool profile | `NmapNarrativeProfile` | Scan/host/trace nugget IDs, labels |
| Integration | `nmap_xml_to_graph.describe_graph` | Replace stats-only markdown |

## Report structure (maximum story)

1. Title + introduction
2. **Scan** — SCAN_RECORD + descriptors + discovered host count
3. **Each host** (scan targets first, then trace-only hosts):
   - Host entity + descriptors
   - Environment (OS, accuracy)
   - Networks (IP → transport → port → state; `listens-to` services)
   - Applications (services, versions, CPE, SSH keys, HTTP titles)
   - Vulnerabilities (when present)
4. **Trace** (if present) — descriptors, ordered hops, Mermaid path diagram
5. Conclusion / scan summary
6. Appendix — every nugget row (type, id, description, value)
7. Footer — OS-Intel Scan, date, page

## Epics and tasks

| ID | Title |
|----|-------|
| Epic | Narrative report generation from semantic graphs |
| Task 1 | Core `SemanticGraph` + `NarrativeReportBuilder` |
| Task 2 | Nmap profile + `describe_graph` integration |
| Task 3 | Tests + capstone reference narrative |
| Task 4 | Regenerate all Nmap scenario `*_description.md` artifacts |

## Verification

- `pytest .tests/test_narrative_report.py`
- `pytest .tests/test_nmap_xml_to_graph.py`
- `validate_narrative_coverage()` — every node `nugget_data` appears in output
