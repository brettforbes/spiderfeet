# SPEC-005 artifact inventory

**Generated:** 2026-07-13 (graph-mandatory cleanup)  
**Machine-readable:** `.governance/project/SPEC005_ARTIFACT_INVENTORY.json`  
**Regenerate:** `python .seed/scripts/cli_corpus/audit_artifact_inventory.py`

## Summary

| Tool | Scenarios | Complete (graph+MD) | Gaps |
|------|-----------|---------------------|------|
| netdiscover | 5 | 5 | — |
| nmap | 60 | 60 | — |
| nerva | 6 | 6 | — |
| nuclei | 5 | 5 | — |
| pius | 6 | 6 | — |
| subfinder | 8 | 8 | — |
| httpx | 8 | 8 | — |
| katana | 2 | 2 | — |
| **Total** | **100** | **100 ok** | **0** |

**Policy:** Graph + narrative Markdown are **mandatory** for every scenario. `graph_deferred` is forbidden. Text-only harvest rows without graphs were removed (`nerva/tcp_http_human_text`, `pius/corporate_bbc_terminal`).

## Path resolution contract (G1)

When resolving graph JSON or narrative Markdown for `(tool_id, scenario_key, scenario_id)`:

1. Bundle-local `proposed_nuggets_edges.json` / `proposed_nuggets_edges_description.md` (if `scenarios/<key>/` layout)
2. `nugget_structure/{tool}_{scenario_id}_proposed_nuggets_edges{.json|_description.md}` — **full manifest id first**
3. `nugget_structure/{tool}_{scenario_key}_proposed_nuggets_edges{...}` — stripped key (suffixes: `_text`, `_json`, `_xml`, `_jsonl`, `_yaml`, `_yml`, `_csv`)
4. Tool-level fallback `nugget_structure/{tool}_proposed_nuggets_edges.json` (graph only, legacy)

## Classification key

| Class | Meaning |
|-------|---------|
| `ok` | structured + graph + markdown on disk |
| `missing-markdown` | graph exists; description missing |
| `missing-graph` | description exists; graph missing |
| `missing-both` | structured exists; neither artifact |
| `partial` | incomplete capture |

## Per-tool notes

- **nmap:** 60 manifests (30 scenario pairs: xml + text). Graph+MD named with full `scenario_id` (e.g. `*_permissive_xml`).
- **katana:** Only 2 examination bundles on disk today (corpus_index notes 8 planned).
- **pius:** `corporate_k2am_ndjson` may use `harvest_deferred` when target offline; graph still required once harvested.

## Scenario matrix (abbreviated — full data in JSON)

See `SPEC005_ARTIFACT_INVENTORY.json` for per-scenario `classification`, resolved paths, and flags.
