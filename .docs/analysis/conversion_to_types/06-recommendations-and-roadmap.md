# Recommendations and roadmap

Make **conversion of unstructured data → typed nuggets** a deliberate platform strength, especially for **CLI expansion** and **knowledge-graph insertion**.

## Design principles

1. **Types are the API** — Modules export observations as nugget types; parsers are implementation detail.
2. **Strings for compatibility, structure for graph** — Keep `SpiderFeetEvent.data: str`; add optional structured fields for TypeDB.
3. **Prove parsers with fixtures** — CLI stdout and API JSON fixtures per module; route seeds prove end-to-end.
4. **Declarative where boring, code where subtle** — JSON field maps and regex tables for 80%; Python for edge cases.

---

## Phase A — Foundation (Stage 5, near term)

### A1. `TypedObservation` helper (non-breaking)

```python
@dataclass
class TypedObservation:
    nugget_id: str
    data: str
    payload: dict | None = None  # structured optional
    confidence: int = 100
```

Module emits via `self.emit(obs, source_event)` wrapping `SpiderFeetEvent` + future payload storage.

**Acceptance:** Template module updated; no change to existing scan DB schema until migration story defined.

### A2. CLI tool base class

Extract from `sfp_tool_nmap`, `sfp_tool_nuclei`, `sfp_tool_testsslsh`:

- Binary resolution (PATH, Windows paths, opts)
- `Popen` + timeout + encoding
- `errorState` on missing binary
- Hook: `parse_stdout(content, source_event) -> list[TypedObservation]`

**Acceptance:** Refactor 2–3 tools as pilots; document parser hook in `conversion_to_types/examples/`.

### A3. Parser fixture tests

Directory: `.tests/fixtures/cli_stdout/<module_id>/`

- `positive.txt` / `positive.jsonl` — minimal output that must yield declared produced types
- Unit test: parser only, no network/subprocess

**Acceptance:** Cover all 13 `sfp_tool_*` modules (including `error` wappalyzer with documented skip).

### A4. Emit-time validation (warn mode)

On `notifyListeners`, log warning if `eventType` not in `nuggets.json` or not in module’s `producedEvents()`.

---

## Phase B — Declarative mapping (medium term)

### B1. API response map spec

YAML alongside module or in `.docs/analysis/conversion_to_types/maps/`:

```yaml
module_id: sfp_shodan
root: "$"
mappings:
  - when: "$.os"
    emit: { nugget_id: OPERATING_SYSTEM, data: "{os} ({addr})" }
  - for_each: "$.data[]"
    emit:
      - { nugget_id: TCP_PORT_OPEN, data: "{addr}:{port}" }
```

Runtime: generic interpreter + Python `post_process` hook.

**Target modules:** High-traffic JSON APIs (Shodan, Censys, SecurityTrails, VirusTotal).

### B2. Regenerate module conversion docs from spec

`analyse_module_conversions.py` reads map spec when present, else falls back to static AST.

---

## Phase C — Knowledge graph nesting (Stage 6+)

See [07-typedb-nesting-relations.md](07-typedb-nesting-relations.md).

### C1. Instance-level relations (not just archetype routes)

- `host-has-ip`, `host-has-open-port`, `port-has-banner`, `service-on-port`
- Populated from structured `payload` during scan ingest or post-scan ETL

### C2. Scan ingest pipeline

Scan completes → normaliser walks events → inserts nugget instances + relations → links to `scan-record`.

### C3. UI: drill-down

Maps tab: expand host node → ports → technologies (from nested relations, not string split).

---

## Phase D — Scanning programme (your stated direction)

### D1. Internal vs external scan lanes

| Lane | Modules | Consumes | Produces |
|------|---------|----------|----------|
| External OSINT | Existing API modules | Seeds from target | Enrichment types |
| Internal active | `sfp_portscan_tcp`, `sfp_tool_nmap`, nuclei, … | `IP_ADDRESS`, netblocks | Ports, OS, vulns |
| Passive local | DNS, SSL, WHOIS | Names, domains | Resolution chain |

Orchestration: composer/sequence (Stage 7+) runs lanes with explicit policies.

### D2. CLI tool expansion playbook

For each new tool:

1. Add `sfp_tool_<name>.py` extending CLI base
2. Implement `parse_stdout` + fixtures
3. Register routes in `osint_services.json`
4. Add map doc under `conversion_to_types/modules/`
5. Route-seed test in `module_test_seeds.json`

### D3. Normalised port/service model

Replace ad hoc `8.8.8.8:443` strings with payload:

```json
{ "ip": "8.8.8.8", "port": 443, "protocol": "tcp", "state": "open" }
```

Emit **both** legacy string and structured payload until graph/UI migrate.

---

## Priority order (recommended)

| Priority | Item | Rationale |
|----------|------|-----------|
| P0 | CLI base + parser fixtures | Unblocks CLI scaling |
| P0 | TypeDB nesting schema (design + spec) | Graph value |
| P1 | Structured payload on events | Enables nesting |
| P1 | Emit validation | Catches drift early |
| P2 | Declarative JSON maps | Reduces duplication |
| P3 | Full ETL ingest | After schema stable |

---

## Success metrics

- New CLI module: **< 1 day** including test fixtures (vs multi-day copy-paste today)
- Parser regression: **fixture tests** per tool, green in CI
- Graph query: “all open ports on hosts affiliated with domain X” without parsing `nugget_data` strings
- Documentation: `conversion_to_types/modules/<id>.md` matches runtime spec or code

---

## Related artefacts

- Architecture: [01-architecture-and-pipeline.md](01-architecture-and-pipeline.md)
- Patterns: [04-conversion-patterns-taxonomy.md](04-conversion-patterns-taxonomy.md)
- TypeQL plan: [07-typedb-nesting-relations.md](07-typedb-nesting-relations.md)
- Stage plan: `.seed/02_stage_by_stage_reengineer.md` (Stage 5+ storage/graph)
