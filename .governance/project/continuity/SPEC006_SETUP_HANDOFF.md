# SPEC-006 setup handoff (2026-07-13)

**Spec:** `.governance/specs/SPEC-006-tool-structure-docs-ontology.md`  
**Plan:** `.governance/project/SPEC006_AGENT_PLAN.md`  
**Quality bar:** `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md`  
**Issue index:** `.governance/project/SPEC006_ISSUE_INDEX.md`

## Intent

Centralize generation of Tools-page **Structure** docs (`*_nugget_graph_structure.md`) to Nmap gold quality, then compose all tool sub-graphs into `_Current_Ontology.md`.

## Pickup for lesser agents

1. Start at **L0** [#992](https://github.com/brettforbes/spiderfeet/issues/992)
2. Follow index order: L → M → N → O
3. Gold example: `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`
4. One issue → one PR to `develop`

## Issue map (created)

| Epic | # | First child |
|------|---|-------------|
| L Quality bar | [#988](https://github.com/brettforbes/spiderfeet/issues/988) | L0 #992 |
| M Engine | [#989](https://github.com/brettforbes/spiderfeet/issues/989) | M1 #995 |
| N Per-tool packs | [#990](https://github.com/brettforbes/spiderfeet/issues/990) | N1 #998 |
| O Ontology compose | [#991](https://github.com/brettforbes/spiderfeet/issues/991) | O1 #1003 |

Full table: `SPEC006_ISSUE_INDEX.md`.

## Not started in this setup turn

Implementation of engine/YAML packs — that is the lesser-agent program.
