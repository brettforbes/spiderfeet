# SPEC-004 setup handoff (2026-07-11)

## Status

Planning artifacts and GitHub issues are **live**. Local implementation has started on
`feature/reengineering-start`; changes are not committed/PR'd yet.

## What lesser agents need

1. Read [proj-07](../../.cursor/rules/proj-07-cli-graph-rules-engine.mdc) + [SPEC-004](../specs/SPEC-004-cli-graph-rules-engine.md)
2. Open [SPEC004_ISSUE_INDEX.md](SPEC004_ISSUE_INDEX.md) and pick the next open child in order
3. Follow the issue body (scope, seeds, forbidden, verification)
4. Branch `feature/<issue>-slug` from `develop`; PR to `develop`

## Already landed in this setup (verify-and-close stories)

|Story|Likely already done|Issue|
|---|---|---|
|A1 SPEC file + BACKLOG|Yes|#911|
|A5 proj-07 + ONBOARDING + templates|Mostly yes (templates + rule + ONBOARDING)|#915|
|A6 doc 14 seed list|Yes|#916|

Progress checkpoints:

- **#912 (A2)** locally complete: `cli_tool_to_graph.py` and `nmap_xml_to_graph.py`
  use shared `graph_builder.nugget_instance_id`; focused graph tests passed.
- **#913 (A3)** locally complete: `core/graph_builder.py` added with old
  `graph_builder.py` compatibility shim; focused graph tests passed.
- **#914 (A4)** in progress: `nuggets_extension.json` catalogue entries added for
  Netdiscover scan/system descriptors and Nerva A/B/C CDN descriptors.
- **#917 (B1)** locally complete: `core/rule_engine.py` loads YAML packs,
  `rules/_shared/` contracts exist, and minimal scan-head graph emission tests passed.
- **#918 (B2)** locally complete: `core/topology.py` and
  `rules/_shared/topology_templates.yaml` define/test shared scan, L2 system,
  host/network/port/service, and trace-hop graph shapes.
- **#919 (B3)** locally complete: `adapters/netdiscover/` exposes the
  `text_native` four-output contract, `rules/netdiscover/` exists, graph output
  uses shared topology helpers, and focused Netdiscover tests passed.

## Four outputs reminder

Text · Structured · Graph · Markdown Report — every formal tool.

## Nerva seeds

- `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`
- `.seed/07B_Nerva_Ontology_Rules.md`

## TypeQL follow-up

A4 extends the JSON nugget catalogue only. Promotion of new catalogue entries such
as `SYSTEM`, `CDN`, Netdiscover scan descriptors, and Nerva correlation/CDN
descriptors into `.seed/spiderfeet_map.tql` remains a follow-up implementation
task unless a later issue explicitly expands TypeQL scope.

## No Nexus
