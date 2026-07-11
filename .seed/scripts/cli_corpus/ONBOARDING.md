# CLI corpus onboarding (SPEC-004)

New CLI apps must follow `.cursor/rules/proj-07-cli-graph-rules-engine.mdc`.

## Checklist

1. Declare `capture_family`: `structured_native` or `text_native`
2. Define intermediate structured schema (or reuse approved bundle shape)
3. Add `rules/<tool>/mapping.yaml` (+ `narrative.yaml`)
4. Optional `adapters/<tool>/hooks.py` with seed rule ids in docstrings
5. Implement `adapters/<tool>/` public API: `to_text`, `to_structured`, `to_graph`, `to_narrative`
6. Wire `harvest.py` to the adapter; emit **four** artifacts
7. Update `nugget_structure/<tool>_nugget_graph_structure.md` and `_Current_Ontology.md`
8. Operator visual review (Epic D7) before golden fixtures
9. Do **not** invent Nexus; do **not** rewrite `sfp_*` until Epic E

## Seeds

See `.governance/specs/SPEC-004-cli-graph-rules-engine.md` seed index (06B, 07, 07B, 08–10, 11, 11B, 14).

## Templates

Copy from `rules/_template/` and `adapters/_template/`.
