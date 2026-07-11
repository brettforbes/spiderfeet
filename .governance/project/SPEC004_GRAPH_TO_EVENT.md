# SPEC-004 graph-to-event bridge design (R4-01-09)

**Issue:** [#953](https://github.com/brettforbes/spiderfeet/issues/953) (E1)  
**Epic:** [#910](https://github.com/brettforbes/spiderfeet/issues/910)  
**Example module shape:** `modules/sfp_abusech.py`

## Problem

CLI Profiling adapters emit a **semantic graph** (`nodes[]`, `edges[]`) under the shared
ontology. Production SpiderFeet modules emit **`SpiderFeetEvent`** instances on a scan bus.
Epic E must connect these without re-embedding mapping logic in each `sfp_tool_*` module.

## Options

### A — Graph-to-event flatten (recommended pilot)

1. Tool subprocess produces structured capture (XML, JSON bundle, NDJSON).
2. Thin module calls `sfp_adapter_bridge.<tool>_graph(...)`.
3. Bridge returns graph dict.
4. Module walks graph and emits one event per **ENTITY** node (descriptors become event
   metadata or child events via existing `sourceEvent` chain).

**Pros:** Single ontology path; adapters stay authoritative.  
**Cons:** Requires flatten policy (which nugget types become events vs stay graph-only).

### B — Dual-emit (defer)

Module emits legacy events *and* stores graph artifact for Maps/TypeDB. Higher duplication;
only consider when a consumer cannot ingest graph shape yet.

## Pilot scope (E2)

- Bridge module: `.seed/scripts/cli_corpus/sfp_adapter_bridge.py`
- Pilot tool: **nmap** (`nmap_graph_from_xml`) — structured XML already supported by adapter
- Unit test proves bridge output matches `adapters.nmap.to_graph`
- **No default behavior change** to `modules/sfp_tool_nmap.py` in pilot PR (still uses `-O`
  text parse); follow-up issues per module under #723 switch scan mode + bridge

## Flatten rules (draft)

| Graph node type | Event strategy |
|-----------------|----------------|
| ENTITY with scan-producing nugget_id | `SpiderFeetEvent(nugget_id, nugget_data, module, sourceEvent)` |
| DESCRIPTOR | Attach to parent entity event as metadata key or skip if redundant |
| CATEGORY | Skip direct emit; used for narrative only |

Exact mapping table to be expanded per tool in follow-up issues.

## Non-goals (pilot)

- Rewriting all quarantine `sfp_tool_*` modules in one PR
- Byte-locked golden events (operator visual review still gates byte fixtures)
- TypeDB persistence of graph (Stage 5+)

## Related

- Bridge API: `sfp_adapter_bridge.py`
- Pattern doc: `.governance/project/SPEC004_SFP_THIN_WRAPPER_PATTERN.md`
- Parent coordination: #723, #796
