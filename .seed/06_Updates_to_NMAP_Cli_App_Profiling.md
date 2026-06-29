# Updates to CLI App Profiling

> **Restored:** 2026-06-27. This operator prompt was deleted during Nmap pilot sign-off (PR #852) after a partial summary was written to `.docs/analysis/cli_profiling_phase2_requirements.md`. Text below is reconstructed from the governed delivery plan, GitHub issues `#830`–`#835` / widget `#70`–`#74`, and implementation artifacts. If you have an earlier local copy, diff and merge any missing operator wording.

**Related:** `.seed/04_Driving and Integrating_CLI_Apps.md` · `.seed/05_Onotology_for_Nuggets.md` · `.cursor/skills/cli_app_profiling/SKILL.md`

---

## 1. Purpose

The Nmap CLI profiling pilot proved the pipeline, but graph generation and the CLI Profiling widget still need ontology alignment, deterministic node identity, richer Nmap script modeling, semantic documentation, graph UX controls, and a full evidence refresh before we move to the next tools in `corpus_index.json`.

This document is the governed update prompt for that work.

---

## 2. Backend — Nugget ontology extensions

Nmap scans expose `ssh-hostkey` script tables and `http-title` output that are not yet represented in the nugget template files or TypeQL schema.

### 2.1 SSH host keys

When Nmap runs `ssh-hostkey` against an open SSH port, model:

- SSH **service** under **APPLICATIONS**
- One **SSH key sub-entity** per returned key (DSA, RSA, ECDSA, ED25519)
- Descriptors for key **type**, **bits**, and **fingerprint/key material**

Add templates to `.docs/analysis/nuggets_extension.json` and matching TypeQL declarations in `.seed/spiderfeet_map.tql`. Use TypeDB 3.8-safe identifiers. New nugget types get **empty** `nugget_icon` until icons exist.

### 2.2 HTTP title

Parse Nmap `http-title` script output into an `http-title` **descriptor** attached to the HTTP **service** node.

---

## 3. Backend — Graph node records and deterministic identity

Generated proposed graph nodes must satisfy the TypeQL nugget model in `.seed/spiderfeet_map.tql` and the field contract in `.seed/05_Onotology_for_Nuggets.md`.

### 3.1 Template-backed nodes

Every node in `*_proposed_nuggets_edges.json` must carry the template fields from:

- `.docs/analysis/nuggets.json`
- `.docs/analysis/nuggets_extension.json`

Do not emit sparse placeholder nodes.

### 3.2 `nugget_instance_id`

Use deterministic UUID5 instance IDs:

- Namespace text: `OS Threat, OS Intel Ontology`
- Seed from canonical `nugget_data`
- Format: `<NUGGET_ID>--<uuid5>`

Widget graph `id` may alias `nugget_instance_id`, but the instance ID must be stable across reruns for the same data.

### 3.3 Data-value normalization

Apply hierarchy-aware value rules:

- **Category / host / trace containers** may use scoped or prefixed values where needed for disambiguation
- **Lower-level entities, subentities, and descriptors** use common unprefixed `nugget_data` values (no artificial uniqueness prefixes)

Reject duplicate edges in generated graphs.

---

## 4. Backend — Nmap XML → graph generation

Update `.seed/scripts/cli_corpus/nmap_xml_to_graph.py`:

1. Parse `ssh-hostkey` script tables into the SSH key subgraph (service → key subentities → type/bits/key descriptors)
2. Parse `http-title` into service descriptors
3. Preserve existing host / port / service / trace modeling

Add focused tests using representative XML that includes port 22 SSH keys and port 80 HTTP titles.

---

## 5. Backend — Semantic graph description markdown

The tool-level graph structure doc (for example `nmap_nugget_graph_structure.md`) describes the app broadly. Operators also need **scenario-specific** plain-language descriptions generated from each scenario graph JSON.

Requirements:

- Deterministic generator producing `*_proposed_nuggets_edges_description.md` from graph `nodes` + `edges`
- Support all Nmap scenario graph JSON files, including `nmap_capstone_permissive_proposed_nuggets_edges.json`
- Describe key node groups and relation patterns without hand-written per-scenario drift
- Expose scenario description markdown through the CLI corpus API for the widget

> **Note:** This section was later extended by ontology §4.3 narrative reports (GitHub `#844`); keep both the statistical/semantic description contract and the §4.3 narrative engine aligned.

---

## 6. Backend — TypeDB query layer (phase 2)

Longer-term ingest and UI graph generation should not depend on ad hoc JSON alone.

- Add TypeQL Fetch / functions for UI graph generation per `.cursor/skills/typedb/SKILL.md`
- Add FastAPI routes that consume those TypeQL graph functions

Track remaining work in `.docs/analysis/cli_profiling_phase2_requirements.md` (GitHub `#851`).

---

## 7. Widget — Profiling Graph tab controls

The CLI Profiling **Graph** tab needs visual simplification without mutating source graph data.

### 7.1 Shadow Descriptors

Add a **Shadow Descriptors** toggle:

- Detect repeated descriptor targets of `had` / `has_this` edges
- Create deterministic shadow nodes for repeated targets
- Toggle off must reverse shadows exactly (round-trip equality)

### 7.2 Shadow Entities

Add a **Shadow Entities** toggle:

- Detect repeated low-level entity targets of `contains` / `contains_this` edges
- Exclude meta nuggets and category nodes
- Same deterministic create/reverse behavior

### 7.3 Legend

Add hide/show control for the graph legend. Preserve layout and fullscreen behavior when toggled.

Reuse shared shadow logic between Profiling and Maps where practical (`Widgets.GraphShadows`).

---

## 8. Widget — Maps graph shadow toggle

On the **Maps** page, add **Shadow Nuggets** for repeated archetype nugget targets in `osint-service` **consumed** / **produced** edges (nodes without `nugget_instance_id` that appear multiple times).

Toggle off must restore the original nodes and edges.

---

## 9. Widget — Layout and graph documentation placement

### 9.1 Examination detail chrome

Remove low-value text rows from the examination detail page:

- Scenario key / target / runtime metadata block
- Duplicate command-line text block

Goal: give the Structured / Data Viewer pane more vertical height.

### 9.2 Tool-level vs scenario-level markdown

- Move **tool-level** nugget graph structure markdown access to the **Tools** table (row action), not buried per scenario only
- Surface **scenario-level** generated graph description markdown in examination detail when the API provides it

Backend should split contracts (`/graph-structure` vs scenario `graph_description_markdown`).

---

## 10. Nmap evidence regeneration and operator review

After backend and widget changes land:

1. Run `python .seed/scripts/cli_corpus/harvest.py --tool nmap`
2. Regenerate all `nmap_*_proposed_nuggets_edges.json` and description markdown artifacts
3. Update corpus index / review status artifacts
4. Run backend CLI corpus tests and widget build
5. Spot-check API detail for `nse_default_permissive` and `capstone_permissive`
6. Prepare operator review handoff

---

## 11. Delivery and verification gates

Follow governed workflow:

- Create GitHub epics/tasks with SPEC_GAP binding to this file
- Branch from `develop`, PR to `develop`, promote to `master` / `main` after each epic gate
- End-of-epic checks:
  - **Ontology:** template + TypeQL validation
  - **Generator:** pytest on `nmap_xml_to_graph.py` fixtures
  - **Widget:** `npm run build`, shadow round-trip fixtures, manual smoke on Profiling + Maps
  - **Evidence refresh:** harvest + `--all` graph regen + API contract tests

---

## 12. Implementation status (2026-06-27)

| Area | Status | Notes |
|------|--------|-------|
| SSH key + http-title ontology | Done | PRs `#836`, `#838` |
| UUID5 + template-backed nodes | Done | Epic 1–2 |
| Semantic / narrative descriptions | Done | `#844`–`#848`, `narrative_report.py` |
| Profiling shadows + legend | Done | widget `#71`, `#73`, `#75` |
| Maps shadow toggle | Done | widget `#72` |
| Detail layout + markdown placement | Done | widget `#74`, backend `#840` |
| Nmap evidence refresh | Done | `#842`, pilot sign-off `#850` |
| TypeDB Fetch / FastAPI graph routes | Open | `#851` phase 2 |
