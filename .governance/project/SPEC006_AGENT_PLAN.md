# SPEC-006 agent plan — tool Structure docs + unified ontology

**Spec:** `.governance/specs/SPEC-006-tool-structure-docs-ontology.md`  
**Quality bar:** `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md`  
**Issue index:** `.governance/project/SPEC006_ISSUE_INDEX.md`  
**Audience:** Lesser agents — **one child issue at a time**  
**Gold example:** `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`

---

## How to pick up work (every agent)

1. Read this plan’s epic section for your issue code + the issue body + SPEC-006 requirement IDs.
2. Read the quality bar + the Nmap gold Structure file end-to-end.
3. Read `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` and `.seed/05_Onotology_for_Nuggets.md` §2–§4.
4. Branch from `develop`: `feature/<issue>-<slug>`.
5. Implement **only** that child scope.
6. Run the verification commands on the issue; paste evidence in the issue comment.
7. Open PR to `develop` linking the issue.
8. **Forbidden:** invent Nexus; rewrite `sfp_*`; put values in Mermaid; claim structures the graphs do not emit; skip graph-mandatory / structured-first laws (proj-06).

---

## Architecture target (do not invent alternatives)

```text
rules/_shared/structure_v1.yaml      → reusable type-relation Mermaid patterns + section order
rules/_shared/topology_templates.yaml → graph topology authority; structure patterns must align
rules/<tool>/structure.yaml          → patterns used, scenario map, field map, specialty sections
rules/<tool>/mapping.yaml            → field→nugget (cite paths; do not fork mappings)
core/structure_doc_engine.py         → render tool Structure MD (+ ontology compose helpers)
render_structure_docs.py             → CLI --tool / --all
nugget_structure/<tool>_nugget_graph_structure.md  → Tools page Structure button
_Current_Ontology.md                 → composed union of all tool sub-graphs
```

**80/20:** Prefer YAML + shared engine. Per-tool code/YAML may only name which patterns apply, scenario coverage, field map, and short factual blurbs cited from seed docs.

---

## Epic map

| Epic | Code | Intent | Children |
|------|------|--------|----------|
| Quality bar + inventory | L | Freeze Nmap bar; gap matrix; templates | L0–L2 |
| Central structure engine | M | YAML → MD generator + tests + CLI | M1–M3 |
| Per-tool structure packs | N | structure.yaml + regenerate all 8 tools | N1–N5 |
| Unified ontology compose | O | Fold seeds + tool packs into `_Current_Ontology.md` | O1–O4 |

**Execution order:**

```text
L0 → L1 → L2
  → M1 → M2 → M3
    → N1 → N2 → N3 → N4 → N5
      → O1 → O2 → O3 → O4 (O4 = operator)
```

L0 may start immediately. M1 must not start before L1 (quality bar) lands. N* must not start before M2 (CLI renderer) is usable. O2 may draft in parallel with N4 after O1 inventory.

---

## Epic L — Quality bar + inventory

### L0 — Gap inventory vs Nmap bar

**Do**

1. Score each existing `*_nugget_graph_structure.md` against `SPEC006_STRUCTURE_QUALITY_BAR.md` (Pass / Fail / Missing).
2. List live topology patterns actually present in each tool’s `proposed_nuggets_edges.json` samples (do not invent).
3. Write results to `.governance/project/SPEC006_STRUCTURE_GAP_INVENTORY.md`.

**Done when:** Gap inventory checked in; every ADAPTER_TOOLS row classified.

**Verify:** File exists; eight tools listed; katana/nuclei marked Missing.

### L1 — Freeze quality bar + section contract

**Do**

1. Confirm `SPEC006_STRUCTURE_QUALITY_BAR.md` matches the Nmap gold file section list (edit only if Nmap itself needs a clarified Q-row).
2. Add `_template/structure.yaml` under `rules/_template/` with comments showing required keys: `tool`, `display_name`, `seed_docs`, `patterns`, `scenarios`, `field_mapping`, `specialty_sections`, `review_notes`.

**Done when:** Template + quality bar are the lesser-agent contract.

**Verify:** Template path exists; ONBOARDING mention can wait for N5.

### L2 — Shared Mermaid pattern library

**Do**

1. Create `rules/_shared/structure_v1.yaml` with named patterns that mirror `topology_templates.yaml` (at least: `scan_head`, `system_l2`, `host_networks_port_service`, `trace_hop_chain`) plus stubs for domain/org/web patterns used by pius/subfinder/httpx/katana/nuclei.
2. Each pattern: list of typed edges (`source`, `relation`, `target`) suitable for Mermaid emission.
3. Document that new patterns require alignment with topology templates or an explicit SPEC note.

**Done when:** Shared YAML loads; patterns cover Nmap + Netdiscover gold diagrams.

**Verify:** Small unit test or script loads YAML and asserts required pattern ids exist.

---

## Epic M — Central structure-doc engine

### M1 — `core/structure_doc_engine.py`

**Do**

1. Implement `render_tool_structure_doc(tool_id) -> str` reading `structure_v1.yaml` + `rules/<tool>/structure.yaml`.
2. Emit Markdown matching Q1–Q13 (title, header, sections, Mermaid from patterns, tables from YAML).
3. Sanitize Mermaid node labels (reject obvious value shapes: IPv4, URLs) in tests.

**Done when:** Engine can render from a minimal fixture structure.yaml in tests.

**Verify:** `pytest .tests/test_structure_doc_engine.py` (create with M1).

### M2 — CLI `render_structure_docs.py`

**Do**

1. Add `.seed/scripts/cli_corpus/render_structure_docs.py` with `--tool` / `--all` writing to `nugget_structure/<tool>_nugget_graph_structure.md`.
2. Dry-run flag optional.
3. Do **not** overwrite until N1 supplies real packs — M2 may write behind a `--force` or only when structure.yaml exists.

**Done when:** CLI documented in ONBOARDING draft comment; callable for tools that have structure.yaml.

**Verify:** `--help` works; dry-run or fixture tool succeeds.

### M3 — Governance tests

**Do**

1. For every tool in `ADAPTER_TOOLS`: structure.md exists; required H2 headings present; at least one ` ```mermaid ` fence; no IP-like literals inside Mermaid blocks.
2. Hook into or sibling of `test_spec004_governance.py` style checks.

**Done when:** Tests fail if Structure doc deleted or gutted.

**Verify:** `poetry run pytest .tests/test_structure_doc_engine.py .tests/test_spec006_structure_docs.py -q`

---

## Epic N — Per-tool packs + regenerate

**Method for every N child**

1. Read tool `mapping.yaml`, seed docs, 1–2 rich `*_proposed_nuggets_edges.json` graphs, and existing Structure MD (if any).
2. Author `rules/<tool>/structure.yaml` selecting shared patterns + specialty sections.
3. Run `render_structure_docs.py --tool <tool>`.
4. Manually diff against Nmap bar; fix YAML (not one-off MD) until Q1–Q13 pass.
5. Confirm Tools API still returns the file (`GET .../graph-structure`).

### N1 — nmap + netdiscover (freeze gold into YAML)

Reproduce Nmap and Netdiscover Structure quality via engine. Prefer fidelity to current gold MD over “simplification.”

### N2 — nerva + pius

Full rewrite to Nmap bar. Nerva: host/port/service (+ CDN if graphs use it). Pius: org/`COMPANY_NAME` / domain / CIDR trees as graphs actually emit.

### N3 — subfinder + httpx

Full rewrite. Domain apex trees; unresolved vs resolved names; httpx URL/tech/CDN descriptors — Mermaid type patterns, not bullet pipelines.

### N4 — katana + nuclei

**Create** Structure docs from scratch (files currently missing). Katana: crawl URL tree. Nuclei: finding/severity/CVE → VULNERABILITIES category patterns as graphs emit.

### N5 — Onboarding + harvest wiring

Update `ONBOARDING.md`, proj-06/07 pointers: formal examination incomplete without Structure doc regenerated from `structure.yaml`. Optional: call render from backfill script.

---

## Epic O — Unified ontology document

### O1 — Ontology source inventory

List seed + catalogue docs that must be cited when composing `_Current_Ontology.md`:

- `.seed/05_Onotology_for_Nuggets.md`
- Tool seeds (`06B`, `07`, `07B`, `08`–`11B`, netdiscover seed, `14`)
- `.docs/analysis/nuggets.json` + `nuggets_extension.json`
- Each tool’s `structure.yaml` / Structure MD

Write `.governance/project/SPEC006_ONTOLOGY_SOURCE_INVENTORY.md`.

### O2 — Composer path

Extend structure engine (or `compose_current_ontology.py`) to regenerate `_Current_Ontology.md` sections:

1. Sub-graph status table (all eight tools)
2. Unified model intro Mermaid (keep existing voice)
3. Per-tool **Sub-graph: \<Tool\>** sections (embed or summarize type Mermaid from structure packs)
4. Composition / correlation overview
5. Expansion checklist

Do not delete qualification hierarchy / NETWORKS backbone without operator approval — **extend**.

### O3 — Land composed ontology

Run composer; edit YAML packs if composition gaps appear; PR the updated `_Current_Ontology.md`.

### O4 — Operator visual review

Checklist: Tools → Structure for each of 8 tools; skim `_Current_Ontology.md` Mermaid. Sign-off comment on issue. No byte-lock required beyond operator OK.

---

## Suggested verification bundle (after N4+)

```bash
poetry run python .seed/scripts/cli_corpus/render_structure_docs.py --all
poetry run pytest .tests/test_structure_doc_engine.py .tests/test_spec006_structure_docs.py .tests/api/test_cli_corpus.py::test_cli_corpus_tool_graph_structure -q
# Manual: ./start.ps1 → Tools → Structure (nmap gold parity spot-check nerva/httpx/katana)
```

---

## Residual risks

- Graph topologies may still be incomplete for a tool — Structure docs must match **actual** graphs; fix adapters/mapping in a separate issue if Mermaid would lie.
- `_Current_Ontology.md` is long — keep per-tool sections focused; deep field tables stay in per-tool Structure docs.
