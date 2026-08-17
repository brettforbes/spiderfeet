# SPEC-019 — Composer refine 2 (identity, Nerva/Nuclei, YAML collectors, domain hierarchy)

**Status:** Ready for lesser-agent execution (CP1+CP2 complete 2026-08-17)
**Source:** `.seed/20_Refine_Composer_2.md` + operator grill 2026-08-17 (identity, GSE, Nuclei, YAML, Company→Domain→Subdomain→URL)
**Created:** 2026-08-17

**Parents (extends; listed rows **overwrite** named prior rules):**
- CLI graph identity — `.governance/specs/SPEC-004-cli-graph-rules-engine.md` R4-01-01
- CLI workflow DSL + GSE — `.governance/specs/SPEC-007-cli-workflow-dsl.md`
- Nuclei batching — `.governance/specs/SPEC-014-*.md` R14-11 (activate on argv path)
- Composer refine 1 — `.governance/specs/SPEC-018-composer-refine.md` (R18-07, R18-04, R18-11 for the rows below)
- YAML layout — `@yaml-workflow-widget/.governance/specs/SPEC-012-LAYOUT-RULES.md`

**Repos in scope:**

| Repo | Role |
|------|------|
| `spiderfeet` | Identity uuid4 + parent cache; host-scoped GSE; Nerva hydrate; Nuclei batching + progress; Company/Subdomain hierarchy; E2E |
| `yaml-workflow-widget` | Collector `dependencies` = exporters only; vertical vs horizontal ports |
| `spiderfeet-widget` | **Out of scope** (batch `i/n` reuses SPEC-018 B2/D1 fields) |

**Issue indexes:**
- Backend A/B/C/F/E — `.governance/project/SPEC019_ISSUE_INDEX.md`
- YAML D — `@yaml-workflow-widget/.governance/project/SPEC019_ISSUE_INDEX.md`
- Agent plan — `.governance/project/SPEC019_AGENT_PLAN.md`

---

## 0. Operator-confirmed decisions (grill, 2026-08-17)

### 0.1 Identity

1. **ENTITY / SUBENTITY / CATEGORY / INTERNAL** use **uuid4** instance ids. **Stop value-dedupe.** Duplicate `(nugget_id, nugget_data)` in one graph is allowed. Node ids remain unique.
2. **DESCRIPTOR** and **DATA** stay **uuid5** `{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}`, unique-by-value.
3. `SCAN_RECORD` is catalogue ENTITY (uuid4). `ROOT` is INTERNAL (uuid4).
4. **Parent-scoped cache** in `GraphBuilder`: key `(parent_id, nugget_id, data)` for uuid4 types. Same parent + same value = one node; different parents = two uuid4 nodes. Topology/adapters pass `parent_id`.
5. **TypeDB persist** stores each scan graph as emitted. **No cross-scan merge** by `(nugget_id, nugget_data)` this spec.
6. **No CLI corpus re-harvest.** Prove with synthetic uuid4 graphs. Do not GSE-assert `ip_port_list` against old nmap corpus graphs as the cartesian proof.

### 0.2 GSE

7. Identity fix is necessary but **not sufficient**. Rewrite GSE so PORT is bound via **HOST → NETWORKS → TRANSPORT → PORT**, not unbounded `HOST --contains*--> PORT`.
8. Nested `for_each` in `spiderfeet_v2/workflow/gse_eval.py` currently recurses with `scope_ids=None`. Fix scoping so children are restricted to the parent’s reachable set.

### 0.3 Nerva

9. Keep `--list` + `line_text` (one `ip:port` per line). Do not switch 12A to comma-joined `-t`.
10. Hydrate `--output` / `-o` like Subfinder/Nmap. Empty stdout + empty output file → **ERROR**, not fake SUCCESS.
11. No Nerva↔Nmap special case. Any `--list`/`-l` consumer can use the same list.
12. When Nerva mints a `DOMAIN_NAME` equal to the scan apex hostname, wrap it with COMPANY. Off-apex CDN/CNAME hostnames do **not** each get a COMPANY.

### 0.4 Nuclei

13. `crawl_urls` = **URL/LINK only** (`LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`). Drop `DOMAIN_NAME` from that selector.
14. `timeout` = **per-batch** (e.g. 300). New `overall_timeout` = step wall-clock (e.g. 3600).
15. Empty `option_passes` stays one full-template family. Batch when URL count **> 20**; 1–20 URLs = one process (`0/1` then `1/1`).
16. Composer `i/n` = `batches_done / batches_total` while RUNNING via existing `input_done` / `input_total`. Still **one workflow step**. Overrides SPEC-018 §0.1 / R18-07 **for Nuclei only**.
17. No host-widget issues this spec.

### 0.5 YAML collectors

18. Collector `dependencies` = **exporters at that rank + previous collector** only (not `atRank.map(s => s.id)`).
19. `followed-by` / `used-by` attach only to **vertical** in/out ports. `semantic-export` only to **horizontal** context ports / collectors.
20. Smoke must assert Nice-DAG `collector.dependencies`, not only `edgeMeta.has`. Mixed-rank: HTTPX `none` + Nmap export → collector has Nmap only.
21. Do not rewrite Nice-DAG expand internals unless a smoke fails after mapper/deps/port-attachment fixes.

### 0.6 Company → domain → subdomain → URL

22. A graph that involves a **scan-apex** `DOMAIN_NAME` must have `COMPANY --contains--> DOMAIN_NAME`. Unknown legal name is allowed.
23. New **COMPANY** ENTITY. Unknown name: `nugget_data = company:{apex}` and no `COMPANY_NAME` child.
24. **COMPANY_NAME** retagged **ENTITY → DESCRIPTOR**. Pius this spec: `COMPANY --had--> COMPANY_NAME` when the org string is known; `COMPANY --contains--> DOMAIN_NAME`. Bounded Pius wrap only.
25. New **SUBDOMAIN** ENTITY. `nugget_data` = FQDN. Flat: `DOMAIN_NAME --contains-->` each SUBDOMAIN.
26. 12A GSE: `apex_domains` = `DOMAIN_NAME`; `subdomains` = `SUBDOMAIN`; `all_domains` = union + workflow targets. Stop using `DOMAIN_NAME_PARENT` to distinguish children. Do not delete `DOMAIN_NAME_PARENT`.
27. HTTPX: keep **HTTP_STATUS_CODE** (not catalogue `HTTP_CODE`). `had` on the website root probed. Probe URL is `LINKED_URL_INTERNAL` contained by that same root.
28. Katana: hostname match. Mint missing SUBDOMAIN. Off-apex → `LINKED_URL_EXTERNAL`.
29. `SCAN_RECORD --contains--> COMPANY` only (not also SUBDOMAIN or internal URLs). Website roots contain their pages.
30. Validator: if a graph has a `DOMAIN_NAME` equal to the scan target/apex, that node must have COMPANY as a `contains` parent. Do not require COMPANY on every incidental hostname.
31. Nmap keeps `INTERNET_NAME` on HOST — out of this invariant.
32. Implement: shared topology helper + Subfinder, HTTPX, Katana, Pius wrap, Nerva apex wrap + validator. dnsx/Nuclei DOMAIN_NAME emitters are follow-up.

---

## 0.1 Root causes (live k2am / SPEC-018 leftovers)

- uuid5 identity collapses `TRANSPORT(tcp)` / `PORT("22")` across hosts → GSE cartesian `ip:port` (13 ports × 2 hosts = 26 fakes).
- Nested GSE `for_each` does not scope children to the parent.
- Nerva writes JSONL to `--output`; stdout empty; hydrate never reads the file → empty SUCCESS graph.
- Nuclei batching exists (SPEC-014, batch size 20) but `step_runner` passes only `argv` + first `target`, so `_collect_urls` sees one URL and one 900s process runs.
- YAML C3 stopped tagging HTTPX/Katana as `semantic-export` but collector `dependencies` still include every step on the rank; unlabeled edges render as `followed-by`.
- Subfinder emits sibling `DOMAIN_NAME` nodes; there is no `SUBDOMAIN` type; seed 09 forbids COMPANY without org evidence.

---

## 1. Objective

Make Composer 12A runs produce **host-scoped, occurrence-true graphs** and **correct downstream lists**: Nerva receives real `ip:port` lines and hydrates `--output`; Nuclei batches URLs with batch `i/n`; the DAG does not draw `followed-by` from non-exporters to collectors; website graphs are `COMPANY → DOMAIN_NAME → SUBDOMAIN → LINKED_URL_INTERNAL`.

## 2. Non-goals

- CLI corpus re-harvest / rewriting historical `nugget_structure/` graph JSON.
- Cross-scan TypeDB entity merge by IP/domain value.
- Host-widget Composer copy (`0/n tools` vs batches).
- Nested SUBDOMAIN trees; deleting `DOMAIN_NAME_PARENT`.
- Switching HTTP facts to catalogue `HTTP_CODE`.
- dnsx / Nuclei adapter DOMAIN_NAME COMPANY wrap (follow-up unless apex validator fails a 12A Nuclei graph).
- Nice-DAG expand/collapse rewrite unless D2 smoke fails.
- Replacing SPEC-017 temps, SPEC-018 persist-before-FINISHED, or Subfinder `export: scan_graph`.

---

## 3. Requirements

### Backend — Epic A (identity + host-scoped GSE)

| ID | Requirement |
|----|-------------|
| R19-01 | **uuid4 + parent cache + validate_graph split.** Both `graph_builder.py` copies (`modules_v2/_core/` and `.seed/scripts/cli_corpus/core/`). ENTITY/SUBENTITY/CATEGORY/INTERNAL mint uuid4; DESCRIPTOR/DATA stay uuid5 unique-by-value. `GraphBuilder.add_node(..., parent_id=)` caches `(parent_id, nugget_id, data)` for uuid4 types. `validate_graph` allows duplicate `(nugget_id, data)` for uuid4 types; still errors on duplicate ids and on duplicate DESCRIPTOR/DATA pairs. Persist stores graphs as-is (no value-collapse on ingest). |
| R19-02 | **Topology parent_id.** Both `topology.py` copies pass `parent_id` when adding NETWORKS / TRANSPORT / PORT / SERVICE / HOST / SCAN_RECORD so intra-host reuse works. |
| R19-03 | **Host-scoped GSE.** Fix nested `for_each` to scope children to the parent’s reachable set. Rewrite 12A `ip_port_list` to bind PORT via HOST → NETWORKS → TRANSPORT → PORT (IP via HOST → NETWORKS). Synthetic two-host graph: `ip:port` count equals real open ports (not cartesian). Do not use old corpus nmap graphs as the cartesian proof. |
| R19-04 | **Docs.** Ontology seed, proj-05, `identity.yaml`, SPEC-004 R4-01-01 superseded note, 12C nested-`for_each` semantics. |

### Backend — Epic B (Nerva hydrate)

| ID | Requirement |
|----|-------------|
| R19-05 | **Hydrate `--output`/`-o`.** After Nerva CLI, read the output file the same way Subfinder/Nmap hydrate `-o`. Empty stdout + empty output file is ERROR, not fake SUCCESS. |
| R19-06 | **Fixture.** `--list` file of `ip:port` lines → fingerprint records. Cartesian regression covered by R19-03. |

### Backend — Epic C (Nuclei batching)

| ID | Requirement |
|----|-------------|
| R19-07 | **Wire list into batching.** `step_runner` passes full `urls=input_values` (not only argv + first target). Batch when `len > 20`. 12A stays one option pass. |
| R19-08 | **Batch progress + timeouts.** `progress_callback` → registry `input_done`/`input_total` as batches. 12A `timeout` = per-batch; add `overall_timeout` as step cap. |
| R19-09 | **Tests + crawl_urls.** Fake 45 URLs → 3 batches; empty Katana still `skip_step`; `crawl_urls` URL/LINK only (drop `DOMAIN_NAME`). |

### YAML widget — Epic D (collectors + ports)

| ID | Requirement |
|----|-------------|
| R19-10 | **Collector dependencies.** `dependencies` = exporting steps at that rank + previous collector. HTTPX/Katana must not appear in Nice-DAG deps. Overrides incomplete SPEC-018 R18-11. |
| R19-11 | **Port geometry.** `followed-by`/`used-by` on vertical CY only; `semantic-export` on CX (inner context child → collector). Expand internals only if smoke fails after R19-10. |
| R19-12 | **Smoke.** httpx/katana absent from `collector.dependencies`; nmap/nerva present as semantic-export; mixed-rank shared collector still on CX. |

### Backend — Epic F (Company / subdomain / URL hierarchy)

| ID | Requirement |
|----|-------------|
| R19-15 | **Catalogue + TypeQL.** Add `COMPANY` and `SUBDOMAIN` (ENTITY) to both `nuggets_extension.json` copies. Retype `COMPANY_NAME` to DESCRIPTOR in `nuggets.json` and catalogue copies (core type correction; explicit exception to “do not patch nuggets.json for tool-specific additions”). Matching TypeQL. Icons: reuse `icon_company_name.svg` for COMPANY; SUBDOMAIN may reuse `icon_domain_name.svg`. |
| R19-16 | **Shared helper.** Both `topology.py` copies: `add_company_domain_tree(builder, scan_id, apex, company_name=None)` → SCAN contains COMPANY, COMPANY contains DOMAIN_NAME, optional COMPANY `had` COMPANY_NAME. Requires R19-01 parent cache. Unknown name: `nugget_data = company:{apex}`. |
| R19-17 | **Subfinder + 12A GSE.** Seed apex is DOMAIN_NAME under COMPANY; each child host is SUBDOMAIN contained by apex. Rewrite `apex_domains` / `subdomains` / `all_domains`. Update `_rules/subfinder/structure.yaml` and `.seed/09_Ontology_For_Subfinder.md`. |
| R19-18 | **HTTPX.** Classify probe host as DOMAIN_NAME vs SUBDOMAIN; `had` HTTP_STATUS_CODE (and existing HTTP_TITLE / tech) on that website root; homepage `LINKED_URL_INTERNAL` contained by that root. Off-apex CNAME stays DOMAIN_NAME without a new COMPANY. |
| R19-19 | **Katana.** Hostname-match URL ownership; mint missing SUBDOMAIN; off-apex → LINKED_URL_EXTERNAL; SCAN does not contain internal URLs. |
| R19-20 | **Pius bounded wrap.** COMPANY head, `had` COMPANY_NAME, `contains` DOMAIN_NAME. No other Pius mapping changes. |
| R19-21 | **Nerva apex wrap.** If a DOMAIN_NAME equals the scan apex/hostname, wrap with COMPANY via the helper. |
| R19-22 | **Validator + synthetic tests.** Apex DOMAIN_NAME without COMPANY parent fails. Subfinder-shaped graph: COMPANY → DOMAIN_NAME → SUBDOMAIN → URL. HTTPX status on website root. Katana pages under matching host. Historical corpus graphs are not this validator’s target. |

### Integration — Epic E

| ID | Requirement |
|----|-------------|
| R19-13 | **E2E smoke evidence** under `.docs/docs-for-cli-tools/SPEC019_E1_E2E_SMOKE.md`: two-host Nmap → Nerva non-empty fingerprints (not cartesian); Nuclei `i/n` batches; no httpx/katana collector edges; Subfinder graph shows COMPANY → DOMAIN_NAME → SUBDOMAIN; HTTPX/Katana URLs hang off website roots. |
| R19-14 | **GOV-08 exploratory review** with scenario matrix. **[OPERATOR GATE]** |

---

## 4. Explicit overwrites

| Prior rule | Overwrite |
|------------|-----------|
| SPEC-004 **R4-01-01**, proj-05, `.seed/05_Onotology_for_Nuggets.md`, `rules/_shared/identity.yaml`: one node per `(nugget_id, nugget_data)` via uuid5 | ENTITY/SUBENTITY/CATEGORY/INTERNAL are occurrence-scoped uuid4; DESCRIPTOR and DATA stay uuid5 unique-by-value |
| GraphBuilder / `validate_graph` duplicate `(nugget_id, data)` error | Allowed for uuid4 types; ids still unique |
| TypeDB ingest collapse by value | Forbidden this spec |
| SPEC-018 §0.1 / R18-07: Composer `0/n` then `n/n` for whole input list | **Nuclei only:** `i/n` is batch progress |
| SPEC-018 R18-04: do not bump timeout until inputs proven | Inputs proven; `timeout` = per-batch; `overall_timeout` = step cap |
| SPEC-018 R18-11: export-only via `edgeMeta` | Also omit Nice-DAG dependencies for non-exporters; port-type rule is mandatory |
| SPEC-014 R14-11 batching | Remains; **must** activate on workflow argv path |
| SPEC-007 / 12A / 12B / 12C: no SUBDOMAIN; children are DOMAIN_NAME + DOMAIN_NAME_PARENT | SUBDOMAIN ENTITY; GSE selects `nugget_id: SUBDOMAIN` |
| Seed 09: no COMPANY without org evidence; root is DOMAIN_NAME | COMPANY always owns the apex; unknown name uses `company:{apex}` |
| Catalogue `COMPANY_NAME` ENTITY | DESCRIPTOR; Pius root is COMPANY |
| HTTPX/Katana: SCAN_RECORD contains every URL/domain | SCAN contains COMPANY; website roots contain pages |

---

## 5. Execution order & dependencies

```
A1 → A2 → A3 → A4
F1 ∥ A1
F2 after A1
F3–F7 after F2 (parallel)
F8 after F3–F7
B1 after A1; B2 after A3
C1 ∥ C2 → C3
D1 → D2 → D3   (yaml-workflow-widget; parallel to backend)
E1 after A3+B2+C3+D3+F8 → E2 operator
```

Hard edges:
- **F2** requires **A1** (parent cache).
- **B2** requires **A3** (host-scoped `ip_port_list`).
- **E1** waits for A3, B2, C3, D3, F8.

## 6. Governance & lesser-agent execution

- One issue at a time **per repo**. Branch from `develop` → PR into `develop` → close with evidence → merge → return to `develop` (GOV-02).
- Read the GitHub issue body + this spec’s requirement ID + `.governance/project/SPEC019_AGENT_PLAN.md`.
- Keep both `graph_builder.py` / `topology.py` copies in sync.
- Do not invent nugget ids outside the catalogue change in R19-15.
- Do not re-harvest corpus. Do not fan-out Nuclei per URL. Do not rewrite GSE to TypeQL.
- Commit/merge only per operator-approved policy.

## 7. Traceability

Requirement IDs `R19-01`…`R19-22` (R19-13/14 are Epic E; R19-15..22 are Epic F). Issues tagged `[SPEC-019]`. Milestone “done” (except E2) = 12A Nerva fingerprints are non-cartesian and hydrated; Nuclei batches with `i/n`; YAML collectors have no HTTPX/Katana `followed-by`; website graphs are COMPANY → DOMAIN_NAME → SUBDOMAIN → URL.
