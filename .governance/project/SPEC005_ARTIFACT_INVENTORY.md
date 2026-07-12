# SPEC-005 artifact inventory

**Generated:** 2026-07-12 (G0 #963)  
**Machine-readable:** `.governance/project/SPEC005_ARTIFACT_INVENTORY.json`  
**Regenerate:** `python .seed/scripts/cli_corpus/audit_artifact_inventory.py`

## Summary

| Tool | Scenarios | Complete (graph+MD) | Gaps |
|------|-----------|---------------------|------|
| netdiscover | 5 | 5 | — |
| nmap | 60 | 60 | — |
| nerva | 7 | 6 | 1 text-only (deferred G2) |
| nuclei | 5 | 5 | — |
| pius | 7 | 6 | 1 text-only (deferred G2) |
| subfinder | 8 | 8 | — |
| httpx | 8 | 8 | — |
| katana | 2 | 2 | — |
| **Total** | **102** | **100** | **2** |

**Finding:** Operator-reported “missing descriptions” for netdiscover text / nerva JSON scenarios were **UI resolution bugs** (detail API did not try full `scenario_id` for markdown) while files existed on disk. G1 fixes that. Only two scenarios truly lack graph+MD: text-only pairs pending G2 policy.

## Path resolution contract (G1 implements)

When resolving graph JSON or narrative Markdown for `(tool_id, scenario_key, scenario_id)`:

1. Bundle-local `proposed_nuggets_edges.json` / `proposed_nuggets_edges_description.md` (if `scenarios/<key>/` layout)
2. `nugget_structure/{tool}_{scenario_id}_proposed_nuggets_edges{.json|_description.md}` — **full manifest id first**
3. `nugget_structure/{tool}_{scenario_key}_proposed_nuggets_edges{...}` — stripped key (suffixes: `_text`, `_json`, `_xml`, `_jsonl`, `_yaml`, `_yml`, `_csv`)
4. Tool-level fallback `nugget_structure/{tool}_proposed_nuggets_edges.json` (graph only, legacy)

`list_scenarios` already tries (2) then (3) for badges. `get_scenario` detail must use the same helper for markdown (fixed in G1).

## Classification key

| Class | Meaning |
|-------|---------|
| `ok` | structured (or text-only deferred) + graph + markdown on disk |
| `missing-text-only` | text capture only; no structured; no graph/md — needs derive or `graph_deferred` |
| `missing-markdown` | graph exists; description missing |
| `missing-graph` | description exists; graph missing |
| `missing-both` | structured exists; neither artifact |

## Operator-reported items (resolved)

| Report | scenario_id | On-disk MD? | Root cause |
|--------|-------------|---------------|------------|
| netdiscover A active text | `local_subnet_active_text` | Yes | UI detail lookup (G1) |
| netdiscover C passive snippet | `passive_snippet_text` | Yes | UI detail lookup (G1) |
| nerva fast/https/list/ssh/http rich | `tcp_*_json` | Yes | UI detail lookup (G1) |
| nerva human HTTP | `tcp_http_human_text` | No | text-only — G2 |
| pius terminal BBC | `corporate_bbc_terminal` | No | text-only — G2 |

## G2 deferred scenarios

| Tool | scenario_id | Paired structured scenario |
|------|-------------|----------------------------|
| nerva | `tcp_http_human_text` | `tcp_http_rich_json` |
| pius | `corporate_bbc_terminal` | `corporate_bbc_gleif_ndjson` |

Policy: mark `graph_deferred: true` with reason; show T+S only in UI unless TextFSM derivation lands later.

## Per-tool notes

- **nmap:** 60 manifests (30 scenario pairs: xml + text). Graph+MD named with full `scenario_id` (e.g. `*_permissive_xml`).
- **katana:** Only 2 examination bundles on disk today (corpus_index notes 8 planned).
- **pius:** `corporate_k2am_ndjson` has graph+MD; target was offline in some harvest runs.

## Scenario matrix (abbreviated — full data in JSON)

See `SPEC005_ARTIFACT_INVENTORY.json` for all 102 rows with `classification`, resolved paths, and flags.
