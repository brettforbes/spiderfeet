# Onboarding a new CLI app (SpiderFeet corpus)

**Goal:** Get from “interesting CLI tool” to four reviewable artifacts in CLI Profiling — Text, Structured, Graph, Markdown — with centralized rules, not a one-off converter.

| Read first | Path |
|------------|------|
| Explore / examine discipline | `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc` |
| Graph + narrative engine rules | `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` |
| Operator architecture guide | `.docs/docs-for-cli-tools/SPEC004_SYSTEM_GUIDE.md` |
| Ontology §4 narrative | `.seed/05_Onotology_for_Nuggets.md` |
| Business conversion overview | `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` |
| Profiling skill | `.cursor/skills/cli_app_profiling/SKILL.md` |

**Do not invent Nexus. Do not rewrite production `sfp_*` in the first wave.**

---

## Mental model (keep this small)

```text
Explore (matrix) → Seed rules (optional) → YAML mapping + narrative
       → thin adapter (parse + cited hooks) → harvest four outputs
       → CLI Profiling visual review → structural tests → (later) sfp bridge
```

| Layer | You add for a new tool | You reuse |
|-------|------------------------|-----------|
| Explore | Matrix, targets, help text, strategy skill | proj-06 lessons |
| Rules | `rules/<tool>/mapping.yaml`, `narrative.yaml` | `rules/_shared/*`, IP classify, narrative engine |
| Adapter | Parse/normalize + optional `hooks.py` | `core/graph_builder`, `topology`, `rule_engine`, `ip_classify` |
| Harvest | Manifest scenarios + one dispatch branch | `harvest.py` `ADAPTER_TOOLS` pattern |
| Evidence | Examination bundles + `nugget_structure/` | backfill script |

**80/20:** Prefer YAML and shared `core/`. Adapter Python is only for parsing and seed-cited exceptions.

---

## Phase 0 — Explore (do not harvest yet)

1. Install/probe the tool; capture help → `.docs/docs-for-cli-tools/cli_help_text/<tool>_cli_help_text.md`.
2. Draft a **semantic outcome matrix** (rich, sparse, clean miss, errors, modes, formats). Every row needs scenario id + target + command family — or a proven limitation.
3. Prefer permissive labs for rich shapes; corporate/CDN for sparse/blocked; vuln labs when CVE/app signal is required.
4. Document stdout vs stderr (findings vs progress) for JSONL tools.
5. Write `.cursor/skills/<tool>/SKILL.md` (+ strategy skill if multi-mode).
6. **Gate:** no `harvest.py` until matrix rows are Demonstrated / Proven limitation / Blocked / Deferred.

See also: `.cursor/skills/cli_app_profiling/references/exploration-examination-lessons.md`.

---

## Structured-first law (read before Phase 1)

If the tool offers structured output (JSON, XML, YAML, CSV, `--json`, `-oX`, `--output ndjson`, etc.), **every formal scenario must use it**. Text is for human reading in the Text pane — derived from structured at harvest, not a separate text-only examination run. Text-native harvest is allowed **only** when the tool has no structured mode (then TextFSM → structured before graph).

**Forbidden:** `pius --output terminal`, nerva without `--json`, or any second scenario that omits structured flags when structured flags exist.

**Graph-mandatory:** every scenario must produce graph + narrative Markdown. `graph_deferred` is forbidden. No graph = useless scenario — do not ship it.

---

## Phase 1 — Decide capture family + schema

Pick exactly one:

| Family | When | Structured pane | Text pane |
|--------|------|-----------------|-----------|
| `structured_native` | Tool emits JSON/XML/JSONL | Normalized single-root JSON/XML (JSONL → `schema` + `records[]` bundle) | **Derived** from structured at harvest |
| `text_native` | No structured mode (TUI only) | TextFSM (or equivalent) → JSON | Native full capture (parser input) |

**JSONL / NDJSON:** never store `.jsonl` as the Structured artifact. Bundle shape:

```json
{
  "schema": "<tool>_…_v1",
  "tool": "<tool>",
  "command": "…",
  "started_at": "…",
  "duration_s": 0,
  "exit_code": 0,
  "record_count": 0,
  "records": []
}
```

Empty `records: []` is valid for clean-miss scenarios.

---

## Phase 2 — Scaffold files (copy templates)

```text
.seed/scripts/cli_corpus/
  adapters/_template/   →  adapters/<tool>/__init__.py  (+ hooks.py if needed)
  rules/_template/      →  rules/<tool>/mapping.yaml
                        →  rules/<tool>/narrative.yaml
  manifests/            →  manifests/<tool>.yaml
```

Optional seed ontology doc: `.seed/<NN>_…_<Tool>.md` (cite rule ids from hooks).

Add corpus entry in `.docs/docs-for-cli-tools/corpus_index.json` (`phase: exploration` → later `formal_examination`).

---

## Phase 3 — Mapping YAML (graph)

In `rules/<tool>/mapping.yaml`:

- Declare `tool`, `capture_family`, `seed_docs`
- Map fields → existing `nugget_id` values from `.docs/analysis/nuggets.json` (+ extension) — **reuse before invent**
- Prefer shared topology templates (`scan_head`, host/system stacks) from `rules/_shared/`
- Any IP field → will be classified at node creation via `classify_ip` (do not hardcode IPv4-only `IP_ADDRESS` for unknown families)

New archetypes: only `.docs/analysis/nuggets_extension.json` (+ TypeQL when promoting).

---

## Phase 4 — Narrative YAML

In `rules/<tool>/narrative.yaml` set at least:

```yaml
tool: <tool>
host_nugget_id: HOST   # or SYSTEM, CDN, COMPANY_NAME, …
meta_concepts: [scan, host]   # add cdn / trace / org as needed
include_trace: false
include_appendix: true
phrasing:
  introduction: >
    Factual one-liner: which tool, how findings hang off categories/meta-concepts.
```

Engine (SPEC-005 target; nmap/netdiscover already rich) must emit:

- Factual intro (types / hierarchy guide)
- Meta-concept sections + category subsections
- Prose → **type-only Mermaid** → optional table
- Full appendix (every `nugget_data`)

Quality bar files to skim:

- `nugget_structure/nmap_*_proposed_nuggets_edges_description.md`
- `nugget_structure/netdiscover_*_proposed_nuggets_edges_description.md`

**Forbidden:** adapter `to_narrative` that only dumps bullet lists of domains/URLs.

---

## Phase 5 — Adapter implementation

Public API (required):

```python
CAPTURE_FAMILY = "structured_native"  # or text_native

def to_structured(...): ...
def to_text(...): ...
def to_graph(...): ...      # RuleEngine + topology + cited hooks; classify_ip for addresses
def to_narrative(...): ...  # shared narrative engine + this tool's narrative.yaml
def build_outputs(...): ... # returns text, structured, structured_json, graph, markdown_report
```

Hooks (`hooks.py`): every function docstring cites a seed rule id (`08 R1`, `07B N1`, …).

Wire into `harvest.py`:

- Add tool id to `ADAPTER_TOOLS`
- Add to `STRUCTURED_NATIVE_ADAPTER_TOOLS` when applicable
- Reuse an existing `_write_adapter_four_outputs` branch pattern

Unit tests: `.tests/test_<tool>_adapter.py` (structured round-trip, graph connectivity, narrative coverage).

---

## Phase 6 — Manifest + formal harvest

1. Author `manifests/<tool>.yaml` scenarios from the exploration matrix.
2. Run:

```bash
python .seed/scripts/cli_corpus/harvest.py --tool <tool> --dry-run
python .seed/scripts/cli_corpus/harvest.py --tool <tool>
# or one scenario:
python .seed/scripts/cli_corpus/harvest.py --tool <tool> --scenario <scenario_id>
```

3. Confirm files:

```text
app_examination_docs/<tool>/<n>_manifest.json
app_examination_docs/<tool>/<n>_command.txt
app_examination_docs/<tool>/<n>_output_text.txt
app_examination_docs/<tool>/<n>_output_structured.json   # or .xml
nugget_structure/<tool>_<scenario_id>_proposed_nuggets_edges.json
nugget_structure/<tool>_<scenario_id>_proposed_nuggets_edges_description.md
nugget_structure/<tool>_nugget_graph_structure.md
```

**SPEC-006:** Tool Structure docs must match the Nmap gold bar (`.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md`). Prefer `rules/<tool>/structure.yaml` + `render_structure_docs.py` once Epic M lands — see `.governance/project/SPEC006_AGENT_PLAN.md`. Also update composed ontology `.docs/docs-for-cli-tools/_Current_Ontology.md` when a new sub-graph lands.

### SPEC-008 content bundle (required before operator review)

Formal examination and onboarding are **incomplete** without a content-platform bundle under `modules_v2/content/<tool_id>/` per `.governance/project/SPEC008_CONTENT_CONTRACT.md`:

```text
modules_v2/content/<tool_id>/
  manifest.json
  options.md
  options_schema.json
  zero_to_hero.md
  graph_structure.md
```

Generate/backfill:

```bash
python .seed/scripts/cli_corpus/backfill_content_bundles.py --tool <tool>
python .seed/scripts/cli_corpus/generate_options_schema.py --tool <tool> --check
```

Resolve every entry in `options_schema.review.md` before marking the bundle Pass. Content is served by `GET /api/v1/content/*` (SPEC-008 R8-04).

4. If graph/MD missing after an engine change but structured exists:

```bash
python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool <tool> --force
```

### Anti-patterns (learned the hard way)

| Don’t | Do |
|-------|-----|
| `structured_ext: jsonl` | Bundle JSON (`structured_ext: json`) |
| `text_from: stderr` for NDJSON findings | Capture stdout findings; stderr as banner only |
| Shell-redirect NDJSON when tool needs TTY | Harvest stdout capture |
| Domain arg as `https://host/` when hostname required | Validate in exploration |
| `wsl --shutdown` then immediate WSL harvest | Avoid; DNS breaks |
| Truncate with `head`/`tail` | Full capture; `timeout` only for bounds |
| Skip empty JSONL as “done” on resume | Force re-run or require stderr sidecar |
| Silent missing Graph/MD | Fix adapter; never skip structured when available |
| Text-only scenario when `--json` / ndjson / `-oX` exists | One structured scenario; derive Text at harvest |
| Hardcoded IPv6 as `IP_ADDRESS` | `classify_ip` |
| Inline stub narratives | Shared engine + YAML |

---

## Phase 7 — Operator review

1. Start UI (`./start.ps1`) → widget **CLI Profiling**.
2. For each scenario: Text / Structured (Data Viewer) / Graph / Markdown.
3. Use `.governance/project/SPEC004_VISUAL_REVIEW_CHECKLIST.md` (and SPEC-005 refinements if open).
4. On approval: `review_status: approved`, `corpus_index.json` phase → `complete`, optional `<tool>_pilot_signoff.md`.

**Do not** byte-lock golden narrative fixtures before visual sign-off.

---

## Phase 8 — Governance tests

```bash
python -m pytest \
  .tests/test_spec004_governance.py \
  .tests/test_spec004_narrative_coverage.py \
  .tests/test_harvest_adapter_dispatch.py \
  .tests/test_<tool>_adapter.py \
  -q
```

Add tool to harvest-dispatch expectations when wiring `ADAPTER_TOOLS`.

---

## Phase 9 — Second push (later)

Thin `modules/sfp_tool_<tool>.py` calling `sfp_adapter_bridge` — only after goldens / operator approval.

Pattern: `.governance/project/SPEC004_SFP_THIN_WRAPPER_PATTERN.md`.

---

## Shared capabilities cheat-sheet

| Need | Use |
|------|-----|
| Node identity / catalogue | `core.graph_builder` |
| Scan head / host stacks | `core.topology` + `rules/_shared` |
| YAML field maps | `core.rule_engine` + `rules/<tool>/mapping.yaml` |
| IPv4 / IPv6 nugget id | `core.ip_classify.classify_ip` + `rules/_shared/ip_patterns.yaml` |
| CDN / ASN lists | `rules/_shared/cdn_signatures.yaml`, `edge_asns.yaml` |
| Narrative Markdown | Shared narrative engine + `rules/<tool>/narrative.yaml` |
| Regenerate graph+MD | `backfill_adapter_four_outputs.py` |
| Correlation (Nerva-class) | `core.correlation_engine` + seeds 07 / 07B |

---

## Reference tools (copy patterns, not prose)

| Tool | Why look here |
|------|----------------|
| nmap | Rich narrative + XML structured_native |
| netdiscover | text_native + TextFSM + SYSTEM hosts |
| nerva | JSONL bundle + CDN correlation + phrasing |
| pius / subfinder / httpx / katana / nuclei | structured_native JSONL→bundle harvest path |

Issue indexes (traceability): `SPEC004_ISSUE_INDEX.md`, `SPEC005_ISSUE_INDEX.md`.
