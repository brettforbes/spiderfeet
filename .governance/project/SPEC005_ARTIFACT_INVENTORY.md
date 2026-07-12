# SPEC-005 artifact inventory

**Generated:** 2026-07-12 (G0 #963, updated G2 #965)  
**Machine-readable:** `.governance/project/SPEC005_ARTIFACT_INVENTORY.json`  
**Regenerate:** `python .seed/scripts/cli_corpus/audit_artifact_inventory.py`

## Summary

| Tool | Scenarios | Complete (graph+MD) | Gaps |
|------|-----------|---------------------|------|
| netdiscover | 5 | 5 | — |
| nmap | 60 | 60 | — |
| nerva | 7 | 6 | 1 deferred (G2) |
| nuclei | 5 | 5 | — |
| pius | 7 | 6 | 1 deferred (G2) |
| subfinder | 8 | 8 | — |
| httpx | 8 | 8 | — |
| katana | 2 | 2 | — |
| **Total** | **102** | **100 ok + 2 deferred** | **0 missing** |

**Finding:** Operator-reported “missing descriptions” for netdiscover text / nerva JSON scenarios were **UI resolution bugs** (G1). Two text-only scenarios are explicitly `graph_deferred` (G2): nerva `tcp_http_human_text`, pius `corporate_bbc_terminal`.

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
| `deferred` | text-only with `graph_deferred: true` — complete without graph/md |
| `missing-text-only` | text only; no `graph_deferred` flag |
| `missing-markdown` | graph exists; description missing |
| `missing-graph` | description exists; graph missing |
| `missing-both` | structured exists; neither artifact |

## Operator-reported items (resolved)

| Report | scenario_id | On-disk MD? | Root cause |
|--------|-------------|---------------|------------|
| netdiscover A active text | `local_subnet_active_text` | Yes | UI detail lookup (G1) |
| netdiscover C passive snippet | `passive_snippet_text` | Yes | UI detail lookup (G1) |
| nerva fast/https/list/ssh/http rich | `tcp_*_json` | Yes | UI detail lookup (G1) |
| nerva human HTTP | `tcp_http_human_text` | No | `graph_deferred` (G2) |
| pius terminal BBC | `corporate_bbc_terminal` | No | `graph_deferred` (G2) |

## G2 deferred scenarios

| Tool | scenario_id | API scenario_key | Paired structured scenario |
|------|-------------|------------------|----------------------------|
| nerva | `tcp_http_human_text` | `tcp_http_human` | `tcp_http_rich_json` |
| pius | `corporate_bbc_terminal` | `corporate_bbc_terminal` | `corporate_bbc_gleif_ndjson` |

Policy: `graph_deferred: true` with reason in manifests and API; `complete=true` when text is captured.

## Per-tool notes

- **nmap:** 60 manifests (30 scenario pairs: xml + text). Graph+MD named with full `scenario_id` (e.g. `*_permissive_xml`).
- **katana:** Only 2 examination bundles on disk today (corpus_index notes 8 planned).
- **pius:** `corporate_k2am_ndjson` has graph+MD; target was offline in some harvest runs.

## Scenario matrix (abbreviated — full data in JSON)

See `SPEC005_ARTIFACT_INVENTORY.json` for per-scenario `classification`, resolved paths, and flags.
