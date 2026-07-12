# SPEC-005 agent plan — narrative v2 + IP classify

**Spec:** `.governance/specs/SPEC-005-narrative-v2-ip-classify.md`  
**Issue index:** `.governance/project/SPEC005_ISSUE_INDEX.md`  
**Audience:** Lesser agents executing one child issue at a time  
**Operator:** Assign the next **Ready** child in index order; do not parallelize stories that share the same files unless noted.

---

## How to pick up work (every agent)

1. Read this plan + the child issue body + SPEC-005 requirements listed on the issue.
2. Read `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` and `.seed/05_Onotology_for_Nuggets.md` §4.1–§4.3.
3. Branch from `develop`: `feature/<issue>-<slug>`.
4. Implement **only** that child scope.
5. Run the verification commands on the issue.
6. Open PR to `develop` linking the issue; comment evidence paths + commands.
7. Do **not** lock byte goldens; do **not** invent Nexus; do **not** rewrite production `sfp_*` modules.

---

## Architecture target (do not invent alternatives)

```text
rules/_shared/ip_patterns.yaml          → core/ip_classify.py
rules/_shared/narrative_v2.yaml         → core/narrative_engine.py
rules/<tool>/narrative.yaml             → thin adapter to_narrative() wrapper
core/topology.py + adapters/*/hooks.py  → call ip_classify when creating IP nodes
harvest / backfill                      → regenerate graph + markdown artifacts
cli_corpus.py                           → resolve scenario keys without dropping format suffixes incorrectly
```

**80/20 rule:** Prefer YAML decision tables and shared Python. Per-tool code may only supply:

- which host entity id (`HOST` vs `SYSTEM`)
- which meta-concepts apply (e.g. CDN for nerva)
- tool-specific phrasing strings
- cited hooks that ontology seeds require (already exist)

---

## Epic map

| Epic | Code | Intent | Children |
|------|------|--------|----------|
| Artifact trust + UI resolution | G | Fix “missing” graph/description in UI; inventory truly missing | G0–G2 |
| IP address ontology | H | Shared IPv4/IPv6 classifier + wire into graph builders | H1–H4 |
| Narrative engine v2 | I | Centralize §4.3 report generation | I1–I5 |
| Adapter cutover + regenerate | J | Thin wrappers + regenerate all MD/JSON | J1–J4 |
| Operator gate | K | Visual re-review before goldens | K1 |

**Execution order:**

```text
G0 → G1 → G2
  → H1 → H2 → H3 → H4
    → I1 → I2 → I3 → I4 → I5
      → J1 → J2 → J3 → J4
        → K1
```

---

## Epic G — Artifact trust

### Why UI shows “missing” descriptions

`cli_corpus.scenario_key_from_id` strips `_text` / `_json` / `_xml` suffixes when grouping scenarios. Graph/markdown files are often named with the **full** `scenario_id` (e.g. `nerva_tcp_http_rich_json_…`). Lookup by stripped key then fails → UI reports no Markdown even when files exist.

### G0 — Inventory + resolution contract

**Do**

1. Script or pytest that for each examination manifest reports: `has_graph`, `has_markdown`, resolved paths tried.
2. Document expected naming: prefer `nugget_structure/{tool}_{scenario_id}_proposed_nuggets_edges{,_description.md}`.
3. Write the resolution algorithm in the issue comment (accepted contract).

**Done when:** Inventory markdown checked in under `.governance/project/SPEC005_ARTIFACT_INVENTORY.md`.

### G1 — Fix CLI corpus path resolution

**Files:** `spiderfeet/api/services/cli_corpus.py`, `.tests/api/test_cli_corpus.py`

**Do:** When resolving graph/markdown, try candidates in order:

1. `{tool}_{scenario_id}_…` (full id from manifest)
2. `{tool}_{scenario_key}_…` (stripped key)
3. Bundle-local files
4. Documented aliases if any

**Done when:** API returns `graph_description_markdown` for netdiscover text scenarios and nerva `*_json` scenarios that have files on disk. Tests cover both suffix and non-suffix cases.

### G2 — Truly missing scenarios policy

**In scope scenarios**

| Tool | Scenario | Today | Required outcome |
|------|----------|-------|------------------|
| nerva | `tcp_http_human_text` | text only, no graph/md | Derive structured from text **or** set `graph_deferred: true` + UI reason |
| pius | `corporate_bbc_terminal` | text only, no graph/md | Same |

**Do not** fake NDJSON. Prefer: TextFSM / terminal parser → structured bundle → adapter `build_outputs`. If derivation is blocked, mark deferred with evidence — never leave silent empty panes.

---

## Epic H — IP classify (central)

### H1 — YAML patterns + `core/ip_classify.py`

Create `rules/_shared/ip_patterns.yaml`:

```yaml
version: 1
patterns:
  ipv4: '^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
  ipv6: >-
    ^((?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}|
    (?:[0-9A-Fa-f]{1,4}:){1,7}:|
    :(?::[0-9A-Fa-f]{1,4}){1,7}|
    (?:[0-9A-Fa-f]{1,4}:){1,6}:[0-9A-Fa-f]{1,4}|
    (?:[0-9A-Fa-f]{1,4}:){1,5}(?::[0-9A-Fa-f]{1,4}){1,2}|
    (?:[0-9A-Fa-f]{1,4}:){1,4}(?::[0-9A-Fa-f]{1,4}){1,3}|
    (?:[0-9A-Fa-f]{1,4}:){1,3}(?::[0-9A-Fa-f]{1,4}){1,4}|
    (?:[0-9A-Fa-f]{1,4}:){1,2}(?::[0-9A-Fa-f]{1,4}){1,5}|
    [0-9A-Fa-f]{1,4}:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|
    :(?:(?::[0-9A-Fa-f]{1,4}){1,6}))$
roles:
  host:
    ipv4: IP_ADDRESS
    ipv6: IPV6_ADDRESS
  internal:
    ipv4: INTERNAL_IP_ADDRESS
    ipv6: IPV6_ADDRESS   # catalogue has no INTERNAL_IPV6; document limitation
  affiliate:
    ipv4: AFFILIATE_IPADDR
    ipv6: AFFILIATE_IPV6_ADDRESS
```

**API (fixed — do not rename):**

```python
def classify_ip(value: str, *, role: str = "host") -> str | None:
    """Return nugget_id or None if not an IP."""

def assert_ip_nugget(value: str, nugget_id: str, *, role: str = "host") -> None:
    ...
```

Strip brackets from `[2001:db8::1]` before match. Prefer colon ⇒ IPv6 path, dots ⇒ IPv4 path (fast gate) then regex confirm.

**Tests:** `.tests/test_ip_classify.py` with fixtures for dotted v4, compressed v6, full v6, hostname rejection, empty string.

### H2 — Wire `core/topology.py`

Replace hard-coded `IP_ADDRESS` with `classify_ip(...)`. Default role `host`. Optional kwargs for affiliate/internal when callers know.

### H3 — Wire all adapter hooks

Touch: `adapters/nmap/hooks.py`, `adapters/netdiscover/**`, `adapters/nerva/hooks.py`, `adapters/httpx/hooks.py`, `adapters/subfinder/hooks.py`, and any pius/katana/nuclei paths that emit IPs.

**Rule:** Never emit `IP_ADDRESS` for a colon-containing address.

### H4 — Regenerate graphs after IP change

Run backfill for tools that can contain IPv6 (`nmap`, `nerva`, `httpx`, `subfinder` at minimum). Spot-check that `IPV6_ADDRESS` appears when v6 literals exist in structured data. If no corpus fixture has v6, add a **unit** fixture graph (do not invent live scan data).

---

## Epic I — Narrative engine v2

### Design law (from operator)

Every section and subsection must contain, in order:

1. **Prose** — simple words connecting the **values** into a short story  
2. **Mermaid** — **types + semantic relations only** (no literal values on nodes)  
3. **Table** — when multiple comparable rows exist (ports, findings, hosts)

Then pack full detail into the **appendix** tables.

**Introduction** must be factual, e.g.:

> The scan used Nuclei. Findings are organised under each host’s SECURITY / Vulnerabilities category; severity buckets and per-record findings are contained there. This report follows Scan → Host (categories) → Trace → Appendix.

### I1 — Shared meta YAML

Create `rules/_shared/narrative_v2.yaml` defining:

- meta_concepts: `scan`, `host`, `system`, `cdn`, `trace`
- default category order under host/system: `ENVIRONMENT`, `NETWORKS`, `APPLICATIONS`, `VULNERABILITIES` (and tool overrides)
- mermaid style: type-relation edges from graph projection
- appendix mode: `table`
- footer: `OS-Intel Scan`

### I2 — Promote engine to `core/narrative_engine.py`

Move/refactor `narrative_report.py` → `core/narrative_engine.py`.

Public API:

```python
def render_narrative(graph: dict, *, tool: str, scenario_key: str, profile: dict | None = None) -> str: ...
def type_relation_mermaid(graph: dict, *, root_ids: list[str] | None = None) -> str: ...
```

Keep `validate_narrative_coverage` and `SemanticGraph`.

Legacy `narrative_report.py` becomes a thin re-export shim (compat for nmap/netdiscover) until J1 deletes duplication.

### I3 — Factual introduction builder

Central function builds intro from:

- `SCAN_TOOL` / tool name
- profile `intro_facts` templates
- ontology hierarchy blurb from shared YAML (types, not values)

### I4 — Type-only Mermaid projector

Implement projection: unique edges as `NUGGET_ID_A -->|relation| NUGGET_ID_B` (sanitize ids for Mermaid). Never put `nugget_data` in Mermaid nodes for section diagrams. Value-labelled diagrams are allowed **only** in appendix if a tool profile explicitly opts in (default off).

### I5 — Wire YAML `sections` (kill dead config)

Engine must **read** `rules/<tool>/narrative.yaml` keys:

- `host_nugget_id`
- `meta_concepts` / `sections`
- `phrasing`
- `include_trace`
- `include_appendix`

Update `_template/narrative.yaml` to the v2 schema. Update ONBOARDING + SYSTEM guide.

---

## Epic J — Cutover + regenerate

### J1 — nmap + netdiscover on v2 engine

Replace dedicated builders with `render_narrative`. Preserve quality; improve Introduction only. Diff sample MD files — structure must remain sectioned with Mermaid + appendix.

### J2 — nerva + pius + subfinder on v2

Delete inline stub `to_narrative` bodies; call engine. Expand YAML profiles for CDN / org meta-concepts.

### J3 — httpx + katana + nuclei on v2

Same as J2. Nuclei intro must mention findings contained under host security/vuln categories (factual).

### J4 — Full corpus regenerate

```bash
python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --force
```

(or harvest per tool). Commit regenerated `nugget_structure/*` with the cutover PR(s). Update `SPEC005_ARTIFACT_INVENTORY.md`.

---

## Epic K — Operator gate

### K1 — Visual re-review

Update `.governance/project/SPEC004_VISUAL_REVIEW_CHECKLIST.md` (or SPEC005 checklist) with pass/fail after v2. Link refinement rows to closed SPEC-005 children. **Do not** enable byte-locked goldens until signed.

---

## Decision rules agents must not reopen

| Topic | Decision |
|-------|----------|
| IPv4 vs IPv6 detection | Shared YAML regex; dots vs colons as fast gate |
| INTERNAL IPv6 | Map to `IPV6_ADDRESS` until catalogue adds INTERNAL_IPV6 |
| Mermaid in body sections | Types + relations only |
| Values | Prose + tables + appendix — not Mermaid labels |
| Capture family | Still `structured_native` / `text_native` per proj-07 |
| Text-only without parser | `graph_deferred` + reason, not silent miss |
| Relations | Still `contains` / `had` / `listens-to` only |

---

## Suggested tests per epic

| Epic | Tests |
|------|-------|
| G | `.tests/api/test_cli_corpus.py` |
| H | `.tests/test_ip_classify.py` + adapter structural checks for nugget_id |
| I | `.tests/test_narrative_engine_v2.py` (section headings, mermaid has no IP literals, coverage) |
| J | Existing `test_*_adapter.py` + `test_spec004_narrative_coverage.py` |
| K | Doc-only + checklist |

---

## Operator assignment cheat-sheet

| Assign this… | When… |
|--------------|-------|
| G0 | First — unblocks truth about missing files |
| G1 | After G0 contract written |
| H1 | Can start after G0 (parallel OK with G1) |
| I1–I2 | After H1 (IP types should appear in regenerated graphs) |
| J* | Only after I5 green |
| K1 | Human only |

Lesser agents: **one issue, one PR**. If blocked, comment on the issue with the blocker issue number and move status to Blocked.
