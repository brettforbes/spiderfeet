# Use Cases and Agent Workflow

## Primary use case (SpiderFeet CLI corpus)

**Given:** CLI text output + target nodes/edges hierarchy  
**Deliver:** Python function using NTC Templates (`parse_output`) that reproduces the target graph

This skill applies during **formal examination** when a tool emits **text-only** output (no JSON/XML).

## End-to-end workflow

```
1. Receive (raw_text, target_nodes_edges) pair(s)
2. Inspect text structure — tables, key-value, multi-line blocks
3. Search stock ntc-templates (unlikely for OSINT) → usually author local template
4. Author .textfsm + index row under project template_dir
5. Validate: python -m textfsm.parser template.textfsm fixture.txt
6. Implement parse_output wrapper → list[dict]
7. Implement to_nodes_edges(rows, seed_id) → match target hierarchy
8. If multiple samples: unify into one function or mode parameter
9. Add unit test with examination fixture
10. Store template path in scenario manifest / nugget_structure doc
```

## Secondary use cases

| Use case | Approach |
|----------|----------|
| Network device show commands | Stock `platform=cisco_ios` etc., `template_dir=None` |
| Netmiko/NAPALM output replay | Same — use device platform slug from index |
| Regression on template change | Re-run fixtures; diff `list[dict]` then graph |
| Operator review rejection | Fix template states; re-harvest structured artifact |

## Integration with CLI profiling phases

| Phase | NTC Templates role |
|-------|-------------------|
| Exploration | Identify if text parsing needed vs JSON |
| Formal examination | Produce `output_structured` via parser or inline JSON from `-json` |
| Nugget proposal | `to_nodes_edges()` must match `proposed_nuggets_edges.json` |
| Operator approve | Template + parser frozen in repo |

## Decision: NTC vs raw TextFSM vs JSON

```
CLI output available?
├─ JSON/XML/YAML → native parser (preferred)
└─ Text only
   ├─ Matches stock NTC platform → parse_output(platform=vendor, ...)
   └─ OSINT / custom → local template_dir + spiderfeet_* platform
        └─ Complex grammar → see textfsm skill for low-level states
```

## Multi-sample unification algorithm

1. Parse all samples to `list[dict]` with candidate templates.
2. If dict keys identical (modulo empty lists) → single template.
3. If keys differ but same tool → mode enum + separate index commands.
4. If graphs merge cleanly with same `to_nodes_edges()` → single function.
5. Else split into `parse_<tool>_<scenario>()` functions — do not over-merge.

## Acceptance criteria

- [ ] `parse_output` succeeds on all provided fixtures
- [ ] No `ParsingException` on examination captures
- [ ] Emitted graph matches target nodes/edges (types + relations)
- [ ] One documented entry point for operators (`parse_to_graph` or module hook)
- [ ] Template + index committed under `.docs/docs-for-cli-tools/textfsm_templates/`
