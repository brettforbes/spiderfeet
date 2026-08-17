# SPEC-019 agent plan — lesser-agent kickoff

**Spec:** `.governance/specs/SPEC-019-composer-refine-2.md`  
**Seed:** `.seed/20_Refine_Composer_2.md`  
**Goal:** uuid4 occurrence identity + parent cache; host-scoped GSE `ip_port_list`; Nerva hydrates `--output`; Nuclei batches URLs with batch `i/n`; YAML collectors omit non-exporters; COMPANY → DOMAIN_NAME → SUBDOMAIN → URL.

## Kickoff order (operator)

Start **one issue at a time** per repo. Preferred first wave (parallel across repos):

| Lane | First issue | Then |
|------|-------------|------|
| Backend identity | **A1** uuid4 + parent cache | A2 → A3 → A4 |
| Backend catalogue | **F1** COMPANY/SUBDOMAIN + COMPANY_NAME retype | F2 after A1 → F3–F7 parallel → F8 |
| YAML | **D1** collector dependencies | D2 → D3 |
| Backend Nerva | **B1** hydrate (after A1) | B2 after A3 |
| Backend Nuclei | **C1** wire urls into batching | C2 → C3 |
| Integration | wait for A3+B2+C3+D3+F8 | E1 → E2 (operator) |

Do **not** start F2 until A1 is on `develop`.
Do **not** start B2 until A3 is on `develop`.
Do **not** start E1 until A3, B2, C3, D3, F8 are on `develop`.
**No `spiderfeet-widget` issues.**

## Per-issue contract

1. Read the GitHub issue body + SPEC-019 requirement ID + this plan’s epic notes.
2. Branch `feature/<n>-<slug>` or `fix/<n>-<slug>` from `develop` only.
3. Smallest coherent change; verify; PR into `develop` with evidence.
4. Comment on the issue at start / blocker / PR / close.
5. Merge, close issue, return repo to `develop` before next issue in that repo.
6. Update the matching `SPEC019*_ISSUE_INDEX.md` status column when closing.

## Skills

- Graph identity / adapters: `.cursor/rules/proj-05-spiderfeet-nugget-ontology.mdc`, `.cursor/rules/proj-07-cli-graph-rules-engine.mdc`
- GSE / workflow YAML: `.seed/12C_Graph_Select_Language.md` — **do not** rewrite GSE to TypeQL
- Nerva / Nuclei / Subfinder / HTTPX / Katana / Pius skills under `.cursor/skills/`
- YAML DAG: `@yaml-workflow-widget/.cursor/skills/nice-dag/SKILL.md`
- Multi-repo paths: `.cursor/skills/cursor-multi-repo/SKILL.md`

## Anti-patterns

- Value-dedupe / uuid5 for ENTITY/SUBENTITY/CATEGORY/INTERNAL
- Cross-scan TypeDB merge by IP/domain this spec
- Corpus re-harvest or rewriting historical `nugget_structure/` graphs
- Unbounded `HOST --contains*--> PORT` GSE after A3
- Nerva SUCCESS graph from empty stdout when `--output` has JSONL
- Nuclei per-URL fan-out or one 900s process over the full `-l` file
- Collector `dependencies = atRank.map(s => s.id)`
- `followed-by` on context (CX) ports
- Inventing nugget ids outside R19-15
- Nested SUBDOMAIN trees; SCAN_RECORD containing every URL
- Switching HTTP facts to catalogue `HTTP_CODE`
- Host-widget Composer work

## Checkpoint status

| CP | Meaning | Status |
|----|---------|--------|
| 1 | Spec + indexes + this plan | **done** (2026-08-17) |
| 2 | GitHub issues open + linked | **done** — A/B/C/F/E [#1308](https://github.com/brettforbes/spiderfeet/issues/1308)–[#1331](https://github.com/brettforbes/spiderfeet/issues/1331); D [#296](https://github.com/brettforbes/yaml-workflow-widget/issues/296)–[#299](https://github.com/brettforbes/yaml-workflow-widget/issues/299) |
| 3 | Implementation complete for review | **done** (2026-08-17) — PRs spiderfeet #1334–#1351; yaml-workflow #301–#305; **E2 #1331 remains operator gate** |

## First issues to assign

1. Backend: [#1309 A1](https://github.com/brettforbes/spiderfeet/issues/1309) and [#1321 F1](https://github.com/brettforbes/spiderfeet/issues/1321) in parallel
2. YAML (parallel): [#297 D1](https://github.com/brettforbes/yaml-workflow-widget/issues/297)
3. After A1: [#1310 A2](https://github.com/brettforbes/spiderfeet/issues/1310), [#1314 B1](https://github.com/brettforbes/spiderfeet/issues/1314), [#1317 C1](https://github.com/brettforbes/spiderfeet/issues/1317); F2 after A1+F1

## Epic notes (for issue bodies)

### Epic A — Identity + host-scoped GSE (`spiderfeet`)

Keep both `graph_builder.py` and `topology.py` copies in sync. A3 must rewrite 12A `ip_port_list` **and** fix nested `for_each` scoping. Synthetic two-host graph is the cartesian proof — not old corpus nmap JSON.

### Epic B — Nerva (`spiderfeet`)

Hydrate is independent of GSE rewrite (B1 after A1). B2 needs A3 so the list file is non-cartesian.

### Epic C — Nuclei (`spiderfeet`)

SPEC-014 batching already exists in `sfp_cli_nuclei.py`; the bug is `step_runner._build_scan_step_spec` not passing `urls`. Progress uses existing `RunRegistry.set_step_input_progress`. Override SPEC-018 “no mid-run i/n” for this module only.

### Epic D — YAML (`yaml-workflow-widget`)

C3 (SPEC-018) only cleared `edgeMeta`. Fix `mapper.js` ~248 `const deps = atRank.map((s) => s.id)`. Smoke must read `collector.dependencies`.

### Epic F — Hierarchy (`spiderfeet`)

F1 is catalogue/TypeQL only and may start with A1. F2 needs A1 parent cache. F3–F7 are adapter wraps using the helper. F8 is the validator — do not run it against historical corpus files.

### Epic E — Integration

E2 is operator-only GOV-08. Lesser agents stop after E1 evidence doc.
