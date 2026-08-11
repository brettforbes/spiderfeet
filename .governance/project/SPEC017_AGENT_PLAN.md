# SPEC-017 agent plan — lesser-agent kickoff

**Spec:** `.governance/specs/SPEC-017-multi-temporary-subgraphs-and-dag-colors.md`  
**Goal:** TypeDB-first multi `temporary_subgraph` + read-only Temporary Subgraph Viewer + YAML DAG color settings.

## Kickoff order (operator)

Start **one issue at a time** per repo. Preferred first wave (parallel across repos):

| Lane | First issue | Then |
|------|-------------|------|
| Backend | **A1** schema repair | A2 ∥ A3 → A4 → A5 → A6 |
| YAML | **C1** status hex+picker | C2 → C3 |
| Host | wait for **A4** merge | B1 → B2 ∥ B3 ∥ B4 |
| Integration | wait for A6+B*+C3 | D1 → D2 (operator) |

Do **not** start host B1 until backend A4 is on `develop`.

## Per-issue contract

1. Read the GitHub issue body + SPEC-017 requirement ID.
2. Branch `feature/<n>-<slug>` or `fix/<n>-<slug>` from `develop` only.
3. Smallest coherent change; verify; PR into `develop` with evidence.
4. Comment on the issue at start / blocker / PR / close.
5. Merge, close issue, return repo to `develop` before next issue in that repo.
6. Update the matching `SPEC017*_ISSUE_INDEX.md` status column when closing.

## Skills

- TypeDB schema: `.cursor/skills/typedb/SKILL.md`
- Multi-repo paths: `.cursor/skills/cursor-multi-repo/SKILL.md`

## Anti-patterns

- Merging into a single uuid5 temporary subgraph
- Client PUT as source of truth for temp graphs
- Using `nugget_instance_id` as canvas node id without `temporary--` remap
- Starting B1 before A4
- Skipping schema attribute definitions / `plays` roles

## Checkpoint status

| CP | Meaning | Status |
|----|---------|--------|
| 1 | Spec + indexes + this plan | **done** (2026-08-12) |
| 2 | GitHub issues open + linked | **done** — A [#1266](https://github.com/brettforbes/spiderfeet/issues/1266)–[#1275](https://github.com/brettforbes/spiderfeet/issues/1275); B [#256](https://github.com/brettforbes/spiderfeet-widget/issues/256)–[#260](https://github.com/brettforbes/spiderfeet-widget/issues/260); C [#274](https://github.com/brettforbes/yaml-workflow-widget/issues/274)–[#277](https://github.com/brettforbes/yaml-workflow-widget/issues/277) |
| 3 | Implementation complete for review | lesser agents + D2 operator gate |

## First issues to assign

1. Backend: [#1267 A1](https://github.com/brettforbes/spiderfeet/issues/1267)
2. YAML (parallel): [#275 C1](https://github.com/brettforbes/yaml-workflow-widget/issues/275) and/or [#276 C2](https://github.com/brettforbes/yaml-workflow-widget/issues/276)
3. Host: only after [#1270 A4](https://github.com/brettforbes/spiderfeet/issues/1270) merges → [#257 B1](https://github.com/brettforbes/spiderfeet-widget/issues/257)
