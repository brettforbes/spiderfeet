# Conversion to types (Nuggets)

**As of 2026-06-11** — analysis of how SpiderFeet modules turn unstructured or semi-structured data into typed **Nuggets** (legacy name: *event types*).

This is the platform capability that bridges OSINT collection, scan orchestration, and the TypeDB knowledge graph.

## Why this matters

SpiderFeet’s differentiator is not merely *fetching* data — it is **classifying** observations into a stable vocabulary (`IP_ADDRESS`, `TCP_PORT_OPEN`, `VULNERABILITY_CVE_HIGH`, …) and linking them in a provenance chain (`sourceEvent`). That vocabulary is what powers:

- module routing (`watchedEvents` / `producedEvents`)
- map visualisation and route testing (Stage 3–4)
- future graph insertion with nested structure (host → ports → services)

## Document map

| Document | Purpose |
|----------|---------|
| [01-architecture-and-pipeline.md](01-architecture-and-pipeline.md) | End-to-end flow: raw input → `SpiderFeetEvent` → storage → map |
| [02-nugget-type-catalog.md](02-nugget-type-catalog.md) | 172 archetype nuggets; ENTITY vs DESCRIPTOR vs DATA |
| [03-parsing-primitives.md](03-parsing-primitives.md) | Shared `sflib` / `helpers` building blocks |
| [04-conversion-patterns-taxonomy.md](04-conversion-patterns-taxonomy.md) | Seven conversion patterns with worked examples |
| [05-generalization-assessment.md](05-generalization-assessment.md) | What can be generic vs module-specific today |
| [06-recommendations-and-roadmap.md](06-recommendations-and-roadmap.md) | Proposed platform improvements (parsers, CLI, graph) |
| [07-typedb-nesting-relations.md](07-typedb-nesting-relations.md) | Planned TypeQL model for systems, IPs, ports |
| [pattern_index.md](pattern_index.md) | Module counts per pattern (auto-generated) |
| [nugget_type_producers.md](nugget_type_producers.md) | Which modules declare each nugget type |
| [modules/](modules/) | **231** per-module conversion summaries |

## Machine-readable index

| File | Contents |
|------|----------|
| `module_conversion_index.json` | Pattern → modules; nugget type → producers |
| `../nuggets.json` | Canonical nugget archetypes (icons, colours, ENTITY/DESCRIPTOR) |
| `../nugget_purposes.json` | Purpose/definition text per nugget (editable; feeds catalog column) |
| `../osint_services.json` | Declared routes (consumes/produces) per OSINT service |

## Regenerate

```powershell
poetry run python .seed/scripts/analyse_module_conversions.py
poetry run python .seed/scripts/generate_nugget_type_catalog.py
```

Static analysis only — it does not execute modules. For behavioural proof use route-seed tests (`module_test_seeds.json`).

## Deep-dive examples

| Example | File |
|---------|------|
| API JSON field mapping | [examples/sfp_shodan.md](examples/sfp_shodan.md) |
| Socket scan → port types | [examples/sfp_portscan_tcp.md](examples/sfp_portscan_tcp.md) |
| CLI stdout line parse | [examples/sfp_tool_nmap.md](examples/sfp_tool_nmap.md) |
| CLI JSON-lines | [examples/sfp_tool_nuclei.md](examples/sfp_tool_nuclei.md) |
| Content extraction | [examples/sfp_email.md](examples/sfp_email.md) |
