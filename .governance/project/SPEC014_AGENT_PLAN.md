# SPEC-014 agent plan — Narrative reports v3 (meta-concept progressive disclosure) + nuclei batching

**Spec:** `.governance/specs/SPEC-014-narrative-meta-concept-reports.md`
**Issue index:** `.governance/project/SPEC014_ISSUE_INDEX.md`
**Audience:** Lesser agents — **one child issue at a time**, fully autonomous unless a hard gate says otherwise.

---

## 0. Autonomous execution protocol (read before picking up any SPEC-014 issue)

The operator has pre-authorized fully autonomous execution for SPEC-014: `develop` on `brettforbes/spiderfeet` has no branch-protection review requirement. This removes the *waiting*, not the *rigor* (GOV-02/04/05/06 still apply).

For **every** SPEC-014 child issue:

1. **Start:** Comment "Starting <code> — <one-line intent>." on the issue.
2. **Branch:** `git checkout develop && git pull && git checkout -b feature/<issue-number>-<slug>`. Branch from `develop` only (GOV-02-GIT-004A). Never stack on another feature branch.
3. **Implement:** Only the scope on the issue. File a separate follow-up issue for adjacent gaps; do not scope-creep.
4. **Verify:** Run every command in the issue's Verification section.
5. **Comment evidence:** Paste the verification pass output as an issue comment before opening the PR.
6. **Commit + push:** Conventional commit referencing the issue number.
7. **PR to `develop`:** `gh pr create --base develop`; body links the issue, cites R14-xx IDs, repeats evidence.
8. **Self-merge:** `gh pr merge --squash --delete-branch` once open (and CI green if configured). Exceptions in §0.1.
9. **Close the loop:** Comment final outcome (PR link, SHA, evidence); confirm the issue closed.
10. **Update the index:** Mark the row `done` (with PR link) in `SPEC014_ISSUE_INDEX.md`.
11. **Return to `develop`:** `git checkout develop && git pull`. Never end parked on a stray branch (GOV-02-GIT-004E/F).
12. **Pick the next unblocked child** in execution order (§2).

### 0.1 Hard gates

- **BA2 (temporary-file sweep)** requires an **explicit operator confirmation comment** listing-approval before deletion. Do not delete files judged "temporary" without it.
- **BF1 (regenerate + review)** is an **operator visual review gate**: regenerate all narratives, post the review index, and **stop** — do not lock byte goldens or start BG1 (modules_v2 parity) until the operator approves the regenerated Markdown.

### 0.2 Forbidden (all SPEC-014 issues)

- Do not add per-tool narrative Python. All narrative logic is in `core/` + declarative `rules/<tool>/narrative.yaml` (R14-07). Adapters keep only the one-line `to_narrative()` shim.
- Do not emit one flat global graph as the primary diagram — use per-meta-concept + per-category diagrams (R14-02/03).
- Do not exceed the diagram shape cap or the example cap; overflow goes to the table (R14-04).
- Do not keep the bespoke `NarrativeReportBuilder` / `NetdiscoverNarrativeReportBuilder` once BD2 lands (R14-06).
- Do not re-scan CLI tools to regenerate narratives — use `backfill_adapter_four_outputs.py --force` (R14-09).
- Do not build a shell-string nuclei execute path — argv arrays only (R14-11).
- Do not diverge `modules_v2` from `.seed/scripts/cli_corpus` without updating `PARITY_DIFFS.md` (R14-10).

---

## 1. Epic map

| Epic | Code | Intent | Children |
|------|------|--------|----------|
| Repo hygiene (precondition) | **BA** | Land pending work in both repos; clean temporary files | BA1, BA2 |
| Registry foundation | **BB** | Shared meta-concept registry aligned with `structure_v1.yaml` | BB1 |
| Central engine | **BC** | `core/meta_narrative.py` + `render_narrative` rewrite | BC1, BC2 |
| Unify nmap/netdiscover | **BD** | Reference snapshot + route through engine + retire bespoke builders | BD1, BD2 |
| Validators + invariant | **BE** | Coverage/meta-concept/size/dedupe validators + max-common gate | BE1, BE2 |
| Regenerate + review | **BF** | `backfill --force` all 8 tools + operator visual review gate | BF1 |
| modules_v2 parity | **BG** | Mirror engine + YAML; parity tests | BG1 |
| Nuclei batching | **BH** | Chunk 15k inputs into blocks of 20 + option-pass fan-out + progress | BH1, BH2 |

## 2. Execution order

```text
BA1 -> BA2 [OPERATOR CONFIRM]           (precondition; orchestrator-preferred)
BB1 -> BC1 -> BC2 -> BD1 -> BD2 -> BE1 -> BE2 -> BF1 [OPERATOR REVIEW] -> BG1
BH1 -> BH2                              (independent lane; may run in parallel after BA)
```

## 3. Active code path vs mirror

- **Active (do first):** `.seed/scripts/cli_corpus/` — this is what `harvest.py`, `backfill_adapter_four_outputs.py`, and the FastAPI service `spiderfeet/api/services/cli_corpus.py` actually read/write. The widget Report tab renders `graph_description_markdown` from that service.
- **Mirror (BG):** `modules_v2/_core` + `modules_v2/_rules`. Keep parity; update `PARITY_DIFFS.md`.

## 4. Per-epic detail

### BA — Repo hygiene (precondition)
- **BA1:** In both `spiderfeet` and `spiderfeet-widget`, land legitimate pending work via governed `feature/`/`docs/` PRs into `develop`; leave each repo clean on `develop`. Do not force-push protected branches.
- **BA2:** Enumerate files that look temporary/scratch (build artifacts, stray exports, editor cruft). Post the list on the issue and **wait for operator confirmation** before deleting; then remove + PR. Do not delete legitimate assets (e.g. copied nugget icons, `.cursor` rules/skills) without confirmation.

### BB — Registry foundation
- **BB1:** Expand `rules/_shared/narrative_v2.yaml` `meta_concepts` into the full model (R14-01), aligned field-by-field with `rules/_shared/structure_v1.yaml` patterns (scan_head, system_l2, host_networks_port_service, domain_apex, org_company_tree, web_url_probe, crawl_url_tree, vuln_findings, trace_hop_chain, os_environment). Add a loader + unit test proving each concept resolves root/category nugget ids and caps. Mirror into `modules_v2/_rules/_shared/` in the same PR to avoid drift, or note the deferral for BG.

### BC — Central engine
- **BC1:** `core/meta_narrative.py` primitives (R14-02): `detect_meta_concepts` (present concepts, ordered), `concept_overview_mermaid` (root -> categories, type-only, capped shapes), `category_example_mermaid` (category -> <= example_cap example instances + `+N more`, descriptor branches once by type), `category_table` (full deduped inventory), `concept_prose` (counts + representative values), `append_appendix` (deduped nodes + edges — fix the duplicate-edge bug seen in the pius example).
- **BC2:** Rewrite the generic path in `core/narrative_engine.py` `render_narrative` to compose sections per R14-03 from the registry, consuming `rules/<tool>/narrative.yaml` overrides only. Keep `type_relation_mermaid` available for the type-only overview but stop using it as the single global diagram.

### BD — Unify nmap/netdiscover
- **BD1:** Snapshot current `nmap_*` and `netdiscover_*` `*_description.md` to a reference fixture dir; define match-or-beat criteria (all prior sections present; `validate_narrative_coverage` passes; per-meta-concept diagrams added).
- **BD2:** Route `render_narrative` for nmap/netdiscover through the shared engine (registry-driven), delete `NarrativeReportBuilder` and `NetdiscoverNarrativeReportBuilder`, and prove the match-or-beat gate. Retain any genuinely tool-specific *mapping* in adapters/rules — only narrative Python is removed.

### BE — Validators + invariant
- **BE1:** Extend `validate_narrative_coverage`; add `validate_meta_concept_coverage`, a mermaid shape-size guard (reuse/adapt `validate_mermaid_purity` for example-mode), example-cap + table-completeness, and appendix-dedupe checks. Unit tests per validator (R14-08).
- **BE2:** Add a max-common invariant test (R14-07): fail if any `adapters/<tool>/__init__.py` defines narrative logic beyond the thin `to_narrative` shim, or if a tool's `narrative.yaml` key is unconsumed by the engine (no dead YAML).

### BF — Regenerate + review
- **BF1:** Run `python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --force` for all 8 tools; verify all validators pass for every scenario; build `.governance/project/SPEC014_REVIEW_INDEX.md` (tool -> scenarios -> notes) and post it. **Operator visual review gate** — stop until approved.

### BG — modules_v2 parity
- **BG1:** Mirror the engine + `narrative_v2.yaml` into `modules_v2/_core` + `modules_v2/_rules`; run/refresh parity tests; update `modules_v2/_core/tests/PARITY_DIFFS.md`.

### BH — Nuclei batching + progress
- **BH1:** In `modules_v2/sfp_cli_nuclei.py`, add a batching orchestrator (R14-11): collect the full target set from `urls`/`hosts`/`host_list`, chunk into blocks of `batch_size` (default 20, spec key `batch_size`), iterate every configured option pass (tags/severity/templates families per `nuclei_strategy`), run nuclei per (pass, block) with argv-only dispatch and per-run timeout, and aggregate all JSONL records into one `nuclei_finding_v1` bundle before the single four-output build. Guard total work with an overall limit/timeout.
- **BH2:** Add progress reporting (R14-12): total = `ceil(len(targets)/batch_size) * option_passes`; emit `batch i/N (pass: tags=..., severity=...)` via an optional callback and accumulate a structured `progress` field (`batches_total`, `batches_done`, `passes`, `bundles_scanned`) on the result; final summary line "bundles scanned across all options: N". Test with a large synthetic input (e.g. 15,000 fake URLs) proving correct block count and progress totals without running the real binary.

## 5. Notes for lesser agents

- Read the epic section above for your code before starting.
- The pius example `pius_corporate_upside_ndjson_..._description.md` is the "before" anti-pattern; `modules_v2/content/<tool>/graph_structure.md` is the hierarchy quality target.
- One issue -> one PR -> self-merge -> comment evidence -> close -> update index -> return to `develop`.
