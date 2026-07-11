# SPEC-004 thin `sfp_*` wrapper pattern (R4-01-09)

**Issue:** [#954](https://github.com/brettforbes/spiderfeet/issues/954) (E3)  
**Design:** [SPEC004_GRAPH_TO_EVENT.md](SPEC004_GRAPH_TO_EVENT.md)  
**Reference module:** `modules/sfp_abusech.py` (API fetch + event notify, no embedded ontology)

## Pattern

```
sfp_tool_<app>                    sfp_adapter_bridge              adapters/<tool>/
     |                                   |                              |
     |-- run CLI / read structured ----->|---- to_structured/to_graph -->|
     |                                   |<------ graph dict ------------|
     |-- flatten graph to events -------->|                              |
     |-- notifyListeners(SpiderFeetEvent) |                              |
```

## Module responsibilities (thin)

1. **meta / opts / optdescs** — unchanged SpiderFeet plugin surface
2. **watchedEvents / producedEvents** — declare consumes/produces from ontology catalogue
3. **handleEvent** — resolve target, invoke tool, capture structured output
4. **Bridge call** — `from sfp_adapter_bridge import nmap_graph_from_xml` (import path TBD per runtime packaging)
5. **Emit** — walk graph entities; `notifyListeners` with provenance

## Forbidden in thin modules

- Duplicate YAML mapping logic (belongs in `rules/<tool>/`)
- Alternate UUID / instance-id helpers
- Full graph builder copies

## Rollout

One GitHub issue per `sfp_tool_*` module under #723. Pilot: nmap XML path (E2 bridge only;
module rewrite is separate issue).

## Verification

- Bridge unit test matches adapter graph
- Module smoke test produces expected event types (follow-up per module)
