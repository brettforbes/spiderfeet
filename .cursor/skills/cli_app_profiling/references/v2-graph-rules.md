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

## Node identity

```python
nugget_instance_id = f"{nugget_id}-{uuid5(namespace, nugget_data)}"
```

## Three-tab output derivation

| Tab | Source |
|-----|--------|
| text | Native CLI text output (or derived from structured) |
| data | JSON/XML/YAML/CSV (or TextFSM-parsed) |
| graph | Module rules applied to structured data |

## Proposal artifacts

- Markdown: `nugget_structure/<tool>_nugget_graph_structure.md` (mermaid + narrative)
- JSON draft: `nugget_structure/<tool>_<exam_id>_proposed_nuggets_edges.json`

Operator approves before ontology promotion.
