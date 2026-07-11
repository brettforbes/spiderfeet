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

## Shared correlation lists (Ruleset C)

Versioned YAML under `rules/_shared/`:

| File | Ruleset | Purpose |
|------|---------|---------|
| `cdn_signatures.yaml` | C1 | Header/banner/technology provider signatures |
| `edge_asns.yaml` | C2 | Known CDN / edge / cloud-proxy ASNs |

**Source of truth:** `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md` (Ruleset C).

**Update process:**

1. Confirm the new vendor/signature/ASN against a real scan record (Nerva/httpx examination artifact or seed appendix).
2. Edit the YAML under `rules/_shared/` — bump `version` and record the change reason in the PR.
3. Add or extend unit tests in `.tests/test_correlation_lists.py` (praetorian/Cloudflare fixtures must keep passing).
4. Do **not** hardcode lists in Python adapters; C2 `correlation_engine.py` loads these files via `core.correlation_lists`.
5. After C3 lands, re-run Nerva structural tests to confirm CDN fronting still classifies correctly.

Loader: `core.correlation_lists.load_cdn_signatures()` / `load_edge_asns()`.

## Narrative profiles (D6)

Each structured-native adapter loads `rules/<tool>/narrative.yaml` and must pass
`validate_narrative_coverage` (every node `nugget_data` appears in the Markdown
appendix). Harvest writes graph + Markdown for all `ADAPTER_TOOLS`, including
pius, subfinder, httpx, katana, and nuclei.

Regression: `.tests/test_spec004_narrative_coverage.py` and
`.tests/test_harvest_adapter_dispatch.py`.

## Nerva narrative phrasing (C4)

`rules/nerva/narrative.yaml` owns CDN / indeterminate-origin wording used by
`adapters.nerva.to_narrative`. Harvest writes the Markdown pane to
`nugget_structure/nerva_<scenario>_proposed_nuggets_edges_description.md`.

When extending phrasing, keep:
- fronted hosts: origin count = indeterminate
- suppressed fingerprints: audit-only, not origin stack claims
- appendix covering every node value (run `validate_narrative_coverage`)

## Templates

Copy from `rules/_template/` and `adapters/_template/`.
