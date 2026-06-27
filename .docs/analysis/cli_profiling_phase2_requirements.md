# CLI Profiling — Phase 2 Requirements

**Status:** Follow-up after Nmap pilot sign-off (`.docs/docs-for-cli-tools/nmap_pilot_signoff.md`)  
**GitHub:** #851  
**Spec:** SPEC_GAP — nugget template parity and TypeDB ingest alignment

## Completed in Nmap pilot (do not re-implement)

- SSH host keys (DSA/RSA/ECDSA/EDDSA) and HTTP title in Nmap graph generation
- Tool-level graph structure doc (`nmap_nugget_graph_structure.md`) + per-scenario narrative reports (§4.3)
- CLI corpus API and widget CLI Profiling tab integration

## Remaining requirements

### Backend — TypeQL and nugget templates

- Align scenario graph nodes with full fields from `.docs/analysis/nuggets.json` + `.docs/analysis/nuggets_extension.json`
- Empty `nugget_icon` for new nugget types until icons exist
- UUID5 `nugget_instance_id` seeded from `nugget_data` (namespace: OS Intel ontology)
- Rules for concatenated vs common `nugget_data` values by hierarchy level (hosts/categories vs attack-surface entities/descriptors)

### Backend — TypeDB query layer

- TypeQL Fetch/functions for UI graph generation per `.cursor/skills/typedb/SKILL.md`
- FastAPI routes consuming TypeQL graph functions

### Widget — Graph UX

- Shadow descriptor / shadow entity toggles for visual simplification
- Shadow OSINT-service relations on Maps page
- Collapsible graph legend
- Graph structure doc on Tools table (not only per-scenario)
- Remove low-value metadata lines above Data Viewer on examination page (key/target/runtime + duplicate command line)

---

_Sourced from operator prompt `.seed/06_Updates_to_Cli_App_Profiling.md` (2026-06); promoted to this durable analysis doc at pilot sign-off. The original seed prompt was restored 2026-06-27 after accidental deletion during sign-off — use the seed file as canonical operator intent; this doc tracks remaining phase-2 gaps only._
