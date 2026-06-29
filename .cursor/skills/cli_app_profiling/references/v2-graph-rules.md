# V2 Graph Rules for CLI Profiling

Source: `.seed/04_Driving and Integrating_CLI_Apps.md` §1.3–1.4

## Scan head

Every examination graph must include a scan entity:

```json
{
  "id": "scan-<uuid>",
  "nugget_id": "SCAN",
  "nugget_type": "ENTITY",
  "attributes": {
    "scan_id": "<OSINT_Service_Name>-<uuid4>",
    "osint_service": "sfp_tool_nmap",
    "command": "<exact command>",
    "target": "<target string>"
  }
}
```

All discovered top-level entities link to the scan with `contains` from scan → entity.

## Relationship vocabulary

| Relation | Use |
|----------|-----|
| `has` | Entity → attribute (port state, product name, confidence) |
| `contains` | Entity → entity (host → networking → ip → protocol → port) |
| `listens on` | Service → port (transitive: host listens on open port) |

## Transitive modelling

- Host `contains` IPAddress even when Networking is the intermediate container.
- Host `listens on` Port when PortState is `open`, even when Service is the direct listener.
- Traces link hosts via IP containment, not raw IP strings alone.

## Do not

- Brute-force every flag permutation
- Skip corporate-target scenarios
- Promote nugget types without evidence bundle
- Run Aircrack-ng until hardware available
- Start formal examination without a completed semantic outcome matrix
- Hard-code `nugget_type` or colours when catalogue entries exist
- Emit duplicate nodes for the same `(nugget_id, nugget_data)`
- Truncate examination output or omit errors from structured artifacts

## Nugget catalogue (mandatory)

Load both files in every graph builder:

| File | Role |
|------|------|
| `.docs/analysis/nuggets.json` | Canonical archetypes (read-only for tool work) |
| `.docs/analysis/nuggets_extension.json` | New tool-specific archetypes |

```python
from graph_builder import load_nugget_templates, nugget_node, GraphBuilder, validate_graph
```

- Resolve `nugget_type`, `nugget_description`, `nugget_colour` from templates.
- New types: add to `nuggets_extension.json` + TypeQL; leave `nugget_icon` empty until icons exist.
- Prefer existing `nugget_id` mappings; justify any unmapped source field in the structure doc.

## Node identity

```python
ONTOLOGY_NAMESPACE = uuid5(NAMESPACE_DNS, "OS Threat, OS Intel Ontology")
nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"
```

Exactly one node per `(nugget_id, nugget_data)` pair in a graph. Reuse the same instance id when the data value repeats; additional owners link via edges (e.g. many `MAC_ADDRESS` → `had` → one `MAC_VENDOR` for `"Unknown"`).

Never emit duplicate instance nodes for the same canonical `nugget_id` + `nugget_data`.

## Connectivity (mandatory)

Every node in `nodes[]` must participate in at least one edge in `edges[]`. Orphan nuggets are invalid.

Graph builders must:

1. Derive ids with uuid5(ontology_seed, nugget_data) and deduplicate nodes by `id`.
2. Validate connectivity and uniqueness after build (fail on orphan, duplicate id, or duplicate nugget_id+data).
3. Attach descriptors with `had` from their owning entity (e.g. `MAC_ADDRESS` → `had` → `MAC_VENDOR`).

## Three-tab output derivation

| Tab | Source |
|-----|--------|
| text | Native CLI text output (or derived from structured) |
| data | JSON/XML/YAML/CSV (or TextFSM-parsed) |
| graph | Module rules applied to structured data |

## Proposal artifacts

- Tool structure: `nugget_structure/<tool>_nugget_graph_structure.md` (mermaid + field mapping; Profiling **Structure** button)
- Per scenario JSON: `nugget_structure/<tool>_<scenario>_proposed_nuggets_edges.json`
- Per scenario narrative: `nugget_structure/<tool>_<scenario>_proposed_nuggets_edges_description.md` (§4.3 in `.seed/05_Onotology_for_Nuggets.md`)

Operator approves before ontology promotion.
