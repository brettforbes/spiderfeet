# SPEC-010 agent plan — SpiderFeet v2 engine (modules_v2, FastAPI, TypeDB)

**Spec:** `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
**Issue index (this repo):** `.governance/project/SPEC010_ISSUE_INDEX.md`
**Companion (widget UI):** `@spiderfeet-widget/.governance/project/SPEC011_AGENT_PLAN.md`
**Source prompt:** `.seed/17_SpiderFeet_v2_Integrating_TypeDB_FastAPI_iFrame.md`
**Skills:** `.cursor/skills/typedb/SKILL.md`, `.cursor/skills/typedb-bridge/SKILL.md`, `.cursor/skills/cli_app_profiling/SKILL.md`
**Audience:** Lesser agents — **one child issue at a time**, fully autonomous unless a hard gate says otherwise.

---

## 0. Autonomous execution protocol (read before picking up any SPEC-010 issue)

The operator has pre-authorized fully autonomous execution: no human review wait before merging to `develop`. This removes the *waiting*, not the *rigor* (GOV-02/04/05/06 evidence standards still apply). For **every** child issue:

1. **Start:** Comment "Starting <code> — <one-line intent>." Move the issue to `In progress` on board #1.
2. **Branch:** `git checkout develop && git pull && git checkout -b feature/<issue-number>-<slug>`. Branch from `develop` only (GOV-02-GIT-004A) — never stack on another feature branch.
3. **Implement:** Only the scope on the issue. Adjacent gaps → note in a comment and file a **separate** follow-up issue; do not scope-creep.
4. **Verify:** Run every command in the issue's Verification section. No skipping.
5. **Comment evidence:** Paste the verification command(s) and pass output as an issue comment **before** the PR.
6. **Commit + push:** Conventional commit referencing the issue number.
7. **PR to `develop`:** `gh pr create --base develop`; body links the issue, cites `R10-*` IDs, repeats verification evidence.
8. **Self-merge:** When the PR is open and any CI is green, `gh pr merge --squash --delete-branch`. Do not wait for a human — except the hard gates in §0.1.
9. **Close the loop:** Comment final outcome (PR link, SHA, evidence); confirm the issue closed.
10. **Update the index:** Mark the row `done` (with PR link) in `SPEC010_ISSUE_INDEX.md`.
11. **Return to `develop`:** `git checkout develop && git pull`. Never end a work unit parked on a stray branch (GOV-02-GIT-004E/F).
12. **Pick the next unblocked child** in execution order (§2) and repeat.

Poetry is the Python runner (`poetry run …`). Live scans are permitted (env has TypeDB + all 8 CLI tools in WSL); prefer permissive/lab targets during unit/integration work and reserve the 4 real example targets for the AP acceptance run.

### 0.1 Hard gates (the only three)

- **G1 — TypeDB `spiderfeet-actual` load/reset (issue AI3 / R10-09).** Creating or `--reset`ting the `spiderfeet-actual` database is destructive. Before the first load, post the exact bootstrap command + confirmation that no existing `spiderfeet-actual` data will be lost, and **wait for an operator approval comment on the AI3 issue.** Subsequent idempotent reloads during the same authorized window do not re-gate.
- **G2 — 8001 API cutover (issue AN1 / R10-23).** Making `spiderfeet_v2` the app served on `127.0.0.1:8001` changes what the running widget talks to. Land the absorb-and-serve change behind an operator approval comment on the AN1 issue, with evidence that the absorbed v1 routes (map/tests/subscriptions/cli-corpus/content) still respond identically. Until approved, run the v2 app on a scratch port for tests.
- **G3 — Final acceptance sign-off (issue AP1 / R10-29).** The live 4-target acceptance run is presented to the operator for sign-off; do not mark the SPEC-010 program `done` without an operator approval comment on AP1.

Everything else proceeds with full autonomy.

### 0.2 Forbidden (all SPEC-010 issues)

- Do not leave any literal `IP_ADDRESS` in emitting/matching code after Epic AH (only intentional legacy locations recorded in the IP migration inventory).
- Do not import from `.seed/scripts/cli_corpus/*` inside `modules_v2/` — the port must be self-contained (R10-10).
- Do not delete the original `.seed/scripts/cli_corpus/` tree.
- Do not add a `typedb-bridge` dependency — `typedb-driver` directly (R10-13).
- Do not build a shell-string command path — argv arrays only.
- Do not touch production v1 `sfp_*` OSINT modules or `sfp-api-*` catalogue.
- Do not break the widget-consumed v1 routes when absorbing them (R10-23/R10-26).
- Do not invent new tool ids — reuse `cli_corpus`/`corpus_index.json` ids.
- Do not mark a scan module "done" while any output form is text-native where a structured mode exists (structured-first law, proj-06).

---

## 1. Epic map

| Epic | Code | Intent | Children |
|------|------|--------|----------|
| IP disambiguation (prereq) | **AH** | Split `IP_ADDRESS` → `IPV4_ADDRESS`/`IPV6_ADDRESS` across canonical stack + regenerate artifacts | AH0–AH4 |
| Schema reconcile + load | **AI** | Edge naming, `relates produced`, `fun` JSON projections, load `spiderfeet-actual` | AI0–AI3 |
| Port corpus → modules_v2/_core | **AJ** | Self-contained `_core` + `_rules` + catalogues + typedb-driver client + parity | AJ1–AJ4 |
| Eight v2 CLI modules | **AK** | `_base` contract + 8 real four-output modules + live smoke | AK0–AK7 |
| TypeDB persistence | **AL** | CRUD + dual-form subgraph serializer + JSON projections | AL1–AL3 |
| Workflow DSL + GSE runtime | **AM** | Parse/validate/schedule + GSE + YAML↔TypeDB + context export/merge | AM1–AM3 |
| FastAPI v2 app | **AN** | Absorb v1 routers on 8001 + new v2 routes + tests | AN1–AN3 |
| Orchestrator | **AO** | Step run + full-workflow chaining | AO1–AO2 |
| Backend acceptance | **AP** | 4-target live run + acceptance script | AP1–AP2 |

## 2. Execution order

```text
AH0 -> AH1 -> AH2 -> AH3 -> AH4            (prerequisite for everything below)

AI0 -> AI1 -> AI2 -> AI3 [G1: DB load]

AJ1 -> AJ2 -> AJ3 -> AJ4                   (after AH; AJ3 client can parallel)
  -> AK0 -> AK1..AK7                       (per-tool, after AJ4)

AL1 -> AL2 -> AL3                          (after AI3 + AJ3)
AM1 -> AM2 -> AM3                          (after AJ4; AM3 needs AL for export persist)

AN1 [G2: 8001 cutover] -> AN2 -> AN3       (after AL + AM)
AO1 -> AO2                                 (after AK + AL + AM)

AP1 [G3: acceptance] -> AP2                (after AN + AO)
```

AH is a hard prerequisite — no engine/module work begins until AH4 lands. AI (schema) can start in parallel with AH but AI4 load waits for AH's schema edits (R10-04). AK modules can be built one tool per issue in parallel once AJ4 lands.

---

## Epic AH — IP_ADDRESS disambiguation

### AH0 — Migration inventory
**Do:** Produce `.governance/project/SPEC010_IP_MIGRATION_INVENTORY.md` — every occurrence of `IP_ADDRESS` (and derived `*_IPADDR` variants) across `.seed/scripts/cli_corpus/**`, `.docs/analysis/nuggets*.json`, `.seed/spiderfeet_v2_semantic.tql`, `.docs/docs-for-cli-tools/**`, `modules_v2/content/**`, generated graph/narrative artifacts. Classify each: `migrate`, `keep-legacy`, `regen-artifact`. Confirm `core/ip_classify.py` already maps literals to ipv4/ipv6 ids.
**Verify:** File checked in; grep counts in the doc match a fresh `rg -c IP_ADDRESS`.

### AH1 — Catalogue split
**Do:** Add `IPV4_ADDRESS` + `IPV6_ADDRESS` to `nuggets_extension.json` (ENTITY; colour/icon; description). Audit `AFFILIATE_IPADDR`/`BLACKLISTED_IPADDR`/`MALICIOUS_IPADDR` per inventory (split or retain). Do not patch `nuggets.json` for new types.
**Verify:** `poetry run python -c "import json;ids={n['nugget_id'] for n in json.load(open('.docs/analysis/nuggets_extension.json'))};assert {'IPV4_ADDRESS','IPV6_ADDRESS'}<=ids"`.

### AH2 — Rules + adapter/topology/correlation code
**Do:** Update `rules/_shared/ip_patterns.yaml` + `core/ip_classify.py` so the host IPv4 role maps to `IPV4_ADDRESS` (not `IP_ADDRESS`), keeping `IPV6_ADDRESS` for colon-form. Update all 8 tools' `rules/<tool>/*.yaml` and `core/topology.py`/`correlation_engine.py`/adapters so address nodes are created only via `classify_ip` → `IPV4_ADDRESS`/`IPV6_ADDRESS`; remove literal `IP_ADDRESS` emission.
**Verify:** `rg "IP_ADDRESS" .seed/scripts/cli_corpus` returns only inventory-approved `keep-legacy` lines.

### AH3 — Schema, structure docs + rule doc
**Do:** Reconcile `.seed/spiderfeet_v2_semantic.tql` to `ipv4-address`/`ipv6-address` consistently; update `.docs/docs-for-cli-tools/nugget_structure/*.md`, `_Current_Ontology.md`, and the `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` IP-addresses table (which currently states host IPv4 = `IP_ADDRESS`).
**Verify:** TypeQL schema parses (typedb skill validate step); docs + proj-07 grep show the split.

### AH4 — Regenerate + re-verify artifacts
**Do:** Regenerate affected graph JSON + narrative MD via `backfill_adapter_four_outputs.py` for all 8 tools and refresh `modules_v2/content/<tool>/graph_structure.md`. Re-run graph validation (no orphan nodes; addresses correctly classified).
**Verify:** `poetry run python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool <each>`; repo-wide `rg IP_ADDRESS` matches only inventory `keep-legacy`.

---

## Epic AI — Schema reconcile + `spiderfeet-actual` load

### AI0 — Edge-naming mapping doc
**Do:** Document the one canonical mapping between graph-JSON relations (`had`/`contains`/`listens-to`) and TypeQL types (`has_this`/`contains_this`/`listens_to_this`); note the seed §3.2 reconciliation. Land as a short design note referenced by AL2.
**Verify:** Note checked in; mapping table complete for all three relations both directions.

### AI1 — `relates produced`
**Do:** Add `scan_step relates produced @card(0..)` and confirm `nugget plays scan_step:produced` round-trips (R10-07).
**Verify:** Schema parses; a define+insert+match smoke inserts a produced nugget and reads it back.

### AI2 — `fun` JSON projections
**Do:** Write the `fun` queries (project, workflow, scan_step, extended `contains_recursive` with `had`/`listens-to`) returning fields sufficient for JSON assembly (R10-08).
**Verify:** typedb skill: run each `fun` against a seeded fixture DB; outputs cover the documented fields.

### AI3 — Bootstrap load `spiderfeet-actual` **[G1]**
**Do:** `spiderfeet_v2/db/bootstrap` loads the reconciled `.tql` into a fresh `spiderfeet-actual` and seeds the 8 `sfp-cli-app-*` services; `--reset` is idempotent. Post the command + no-data-loss confirmation; wait for operator approval comment.
**Verify:** After approval: `poetry run python -m spiderfeet_v2.db.bootstrap --reset` then a ping/read confirms schema + 8 services present.

---

## Epic AJ — Port corpus → `modules_v2/_core`

### AJ1 — Port `_core` engines
**Do:** Copy `cli_corpus/core/*` into `modules_v2/_core/` with imports rewritten to `modules_v2._core.*`; include `narrative_report.py`. No import from `.seed/scripts/cli_corpus`.
**Verify:** `poetry run python -c "import modules_v2._core"` clean; `rg "cli_corpus" modules_v2` returns nothing.

### AJ2 — Port `_rules` + catalogues
**Do:** Copy rule packs to `modules_v2/_rules/` (`_shared/` + per-tool) and make `_core` resolve them from within `modules_v2/`; make `graph_builder` load `nuggets.json`+`nuggets_extension.json` from a single configurable path under `modules_v2/`.
**Verify:** `_core` loads all rule packs + catalogues without reaching outside `modules_v2/`.

### AJ3 — typedb-driver client
**Do:** `spiderfeet_v2/db/connection.py` + `config.py` mirroring `spiderfeet/map/`, targeting `spiderfeet-actual` (config via `.config/typedb.connection.json` / env). typedb-driver directly.
**Verify:** `poetry run python -m spiderfeet_v2.db --ping-only` connects (or reports clearly if server down).

### AJ4 — Parity harness
**Do:** For each of the 8 tools, run ported `_core` over a recorded structured fixture and diff graph+narrative against the original `cli_corpus` output (accounting for the AH IPv4/IPv6 split). Document any explained differences.
**Verify:** `poetry run pytest modules_v2/_core/tests/test_parity.py -q` green for all 8.

---

## Epic AK — Eight v2 CLI modules

### AK0 — `_base` contract + nmap rewrite
**Do:** `modules_v2/_base.py` (four-output `run()` contract, status/counts/duration/timestamp). Rewrite `modules_v2/sfp_cli_nmap.py` to real four-output code using `_base`+`_core`; fix its current syntax errors.
**Verify:** `poetry run python -c "import modules_v2.sfp_cli_nmap"` clean; nmap live smoke against `scanme.nmap.org` yields four forms.

### AK1–AK7 — One issue per remaining tool
**Do (each):** Implement `modules_v2/sfp_cli_<tool>.py` (netdiscover, nerva, pius, subfinder, httpx, katana, nuclei — nmap done in AK0) per `_base`, producing four forms from a live CLI run via `_core`, honouring structured-first.
**Verify (each):** Import-clean; live smoke on a permissive/lab target; four forms present; structured-first respected; graph has no orphan/`IP_ADDRESS` nodes.

---

## Epic AL — TypeDB persistence

### AL1 — Entity CRUD
**Do:** `spiderfeet_v2/db/` CRUD for project/workflow/target/scan_step/subgraph subtypes, each ↔ JSON.
**Verify:** `poetry run pytest spiderfeet_v2/db/tests/test_crud.py -q` against a scratch DB.

### AL2 — Dual-form subgraph serializer
**Do:** One serializer/deserializer bridging graph JSON ↔ TypeDB in-graph form, storing both the `json-string` attribute and the entity/relation form (R10-18), using the AI0 edge mapping.
**Verify:** Round-trip test: JSON graph → store (both forms) → read back → equal.

### AL3 — JSON projection functions
**Do:** Python wrappers over the AI2 `fun` queries returning project/workflow/scan_step JSON; scan_step round-trips its four UI forms + consumed/produced nuggets losslessly.
**Verify:** `poetry run pytest spiderfeet_v2/db/tests/test_projections.py -q`.

---

## Epic AM — Workflow DSL + GSE runtime

### AM1 — Parse/validate/schedule + GSE
**Do:** Integrate `.seed/scripts/cli_workflow/` into `spiderfeet_v2/workflow/`: validate against `workflow_v1.schema.json`/`gse_v1.schema.json`, schedule the `needs` DAG, resolve `input.from`, build argv/files, evaluate `output.vars` GSE against a step scan graph. Canonical shape = 12A.
**Verify:** `poetry run pytest spiderfeet_v2/workflow/tests/test_dsl.py -q` including the 12A example.

### AM2 — YAML ↔ TypeDB conversion
**Do:** Convert a workflow's TypeDB form (workflow/scan_step/target + `*_yaml` attrs) ↔ YAML-DSL/JSON, both directions consistent.
**Verify:** Round-trip: YAML → TypeDB → YAML equals canonical; TypeDB → JSON matches API shape.

### AM3 — Context export + merge
**Do:** `context.export: scan_graph` marks a scan_result_graph for temporary-context export; append-unique merge (unique nodes by id, unique edges by `(source,target,relation)`).
**Verify:** Test merging two overlapping scan graphs yields deduped nodes/edges.

---

## Epic AN — FastAPI v2 app

### AN1 — Absorb v1 + serve on 8001 **[G2]**
**Do:** `spiderfeet_v2/api/` app mounts the existing v1 routers the widget uses (map/tests/subscriptions/cli-corpus/content) and becomes the 8001 app. CORS retained. Behind operator approval comment on AN1.
**Verify:** After approval: start v2 app; `curl` each absorbed route returns the same shape as v1; regression pytest green.

### AN2 — New v2 routes
**Do:** projects/workflows/targets CRUD, workflow/step execute, scan_step retrieval (four forms), temporary/project context read + temporary-context update (strip `temporary_id`, remap to `nugget_instance_id`, R10-25). Pydantic + OpenAPI examples.
**Verify:** `poetry run pytest spiderfeet_v2/api/tests/test_v2_routes.py -q`; `/docs` shows examples.

### AN3 — Route tests + v1 regression
**Do:** pytest for all new routes + regression proving absorbed v1 routes unaffected (R10-26).
**Verify:** Full API suite green.

---

## Epic AO — Orchestrator

### AO1 — Single-step run
**Do:** resolve inputs → invoke module (AK) → capture four forms → persist scan_step + scan_result_graph (AL) → evaluate output.vars (AM) → export to temporary context when `scan_graph`. Record status lifecycle.
**Verify:** Run one subfinder step live; scan_step persisted with four forms; output vars populated.

### AO2 — Full-workflow chaining
**Do:** chain by `needs`, thread prior output vars into later `input.from`, accumulate exported graphs into the project temporary context.
**Verify:** Run the 12A workflow (subfinder→nmap→nerva / subfinder→httpx→katana→nuclei) on a lab/permissive target; all steps persist; temporary context accumulates.

---

## Epic AP — Backend acceptance

### AP1 — 4-target live run **[G3]**
**Do:** Run 12A end-to-end against sbs.com.au, k2am.com.au, venturecapitalopportunitiesfund.com.au, squarepeg.vc. Capture an evidence bundle (per-step four forms, persisted subgraphs, temporary-context contributions). Present for operator sign-off.
**Verify:** Evidence bundle checked in under `spiderfeet_v2/acceptance/`; operator approval comment on AP1.

### AP2 — Acceptance script
**Do:** `spiderfeet_v2/acceptance/run_four_targets.py` reproduces the run and asserts: no `IP_ADDRESS` nodes, no orphans, four-form storage, queryable project/workflow/step/context JSON via API.
**Verify:** `poetry run python spiderfeet_v2/acceptance/run_four_targets.py --target <one>` passes assertions.

---

## Definition of done (program)

- [ ] AH0–AH4 merged; no non-legacy `IP_ADDRESS` remains; artifacts regenerated + verified
- [ ] AI3 loaded `spiderfeet-actual` with operator G1 approval
- [ ] AJ/AK merged; `modules_v2` self-contained; 8 modules produce four forms on live scans
- [ ] AL/AM merged; subgraphs dual-form persisted; DSL+GSE runtime + context merge working
- [ ] AN merged with operator G2 approval; v1 routes unaffected on 8001; v2 routes live + tested
- [ ] AO merged; 12A workflow chains end-to-end on a lab target
- [ ] AP acceptance run signed off (G3) for the 4 targets
- [ ] `SPEC010_ISSUE_INDEX.md` all rows `done` with PR links
- [ ] Continuity note written; SPEC-011 unblocked on the AN2 API contract
