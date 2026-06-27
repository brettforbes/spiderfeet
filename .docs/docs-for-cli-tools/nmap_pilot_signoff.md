# Nmap CLI Profiling Pilot — Operator Sign-Off

**Date:** 2026-06-26  
**Epic:** GitHub #850 · **Parent program:** #826 (CLI Profiling V2 ontology discovery)  
**Spec:** `.seed/04_Driving and Integrating_CLI_Apps.md`, `.seed/05_Onotology_for_Nuggets.md` §4.3

## Outcome

Nmap is the **first completed CLI application profiling pilot**. All formal examination scenarios are **operator-approved**. Evidence bundles, semantic graph proposals, narrative reports, and graph-structure documentation are in-repo and exposed via `GET /api/v1/cli-corpus/*` for the widget **CLI Profiling** tab.

## Approved scenarios (15)

| Scenario key | Target class | Artifacts |
|--------------|--------------|-----------|
| `host_discovery_permissive` | Permissive | text, XML, graph, narrative |
| `host_discovery_corporate` | Corporate | text, XML, graph, narrative |
| `host_discovery_local_subnet` | Local L2 | text, XML, graph, narrative |
| `tcp_top_ports_permissive` | Permissive | text, XML, graph, narrative |
| `tcp_top_ports_corporate` | Corporate | text, XML, graph, narrative |
| `tcp_top_ports_local` | Local L2 | text, XML, graph, narrative |
| `service_version_permissive` | Permissive | text, XML, graph, narrative |
| `service_version_corporate` | Corporate | text, XML, graph, narrative |
| `os_aggressive_permissive` | Permissive | text, XML, graph, narrative |
| `nse_default_permissive` | Permissive | text, XML, graph, narrative |
| `udp_top_permissive` | Permissive | text, XML, graph, narrative |
| `traceroute_permissive` | Permissive | text, XML, graph, narrative |
| `skip_ping_permissive` | Permissive | text, XML, graph, narrative |
| `capstone_permissive` | Permissive (max breadth) | text, XML, graph, narrative |
| `windows_enrich_local` | Local host enrich | text, XML, graph, narrative |

Legacy numbered examination files (60 bundles: XML + text pairs across harvest reruns) share review status per scenario key via `set_review_status()`.

## Deliverables

| Artifact | Location |
|----------|----------|
| Harvest manifest | `.seed/scripts/cli_corpus/manifests/nmap.yaml` |
| Evidence bundles | `.docs/docs-for-cli-tools/app_examination_docs/nmap/` |
| Graph structure | `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md` |
| Per-scenario graphs | `.docs/docs-for-cli-tools/nugget_structure/nmap_<scenario>_proposed_nuggets_edges.json` |
| Narrative reports | `.docs/docs-for-cli-tools/nugget_structure/nmap_<scenario>_proposed_nuggets_edges_description.md` |
| Narrative engine | `.seed/scripts/cli_corpus/narrative_report.py` |
| XML → graph | `.seed/scripts/cli_corpus/nmap_xml_to_graph.py` |
| Operator handoff | `.docs/docs-for-cli-tools/nugget_structure/nmap_narrative_report_handoff.md` |
| Corpus index | `.docs/docs-for-cli-tools/corpus_index.json` (`nmap.phase`: `complete`) |

## Verification evidence

```bash
python -m pytest .tests/test_narrative_report.py .tests/test_nmap_xml_to_graph.py .tests/api/test_cli_corpus.py -q
python .seed/scripts/cli_corpus/nmap_xml_to_graph.py --all
```

- Narrative coverage: `validate_narrative_coverage()` passes on all 15 scenario graphs.
- Widget: CLI Profiling → Nmap → scenario detail (Structured, Graph, Graph description); Mermaid trace diagrams render in capstone/traceroute scenarios.

## Next CLI tool

Follow `corpus_index.json` priority **2: netdiscover**. Reuse this pilot pattern:

1. Exploration → formal plan → `harvest.py` → nugget structure doc → operator review → sign-off doc.

## Follow-up (not blocking pilot)

Phase-2 nugget template alignment (UUID5 instance IDs, full `nuggets.json` field parity in graph nodes, widget UX tweaks): GitHub #851 · `.docs/analysis/cli_profiling_phase2_requirements.md`
