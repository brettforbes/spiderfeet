# SPEC-017 A1 — Schema reload notes

**Issue:** [#1267](https://github.com/brettforbes/spiderfeet/issues/1267)  
**File:** `.seed/spiderfeet_v2_semantic.tql`

## Changes

- `temporary_subgraph` owns `scan_name`, `scan_description`; relates `scan_step` + `project as owner`
- `target_context` owns `nugget_type`, `target_description` (attrs already existed)
- `target` owns `target_nugget_type`
- Attribute defs added: `scan_name`, `scan_description`, `target_nugget_type`
- `scan_step plays temporary_subgraph:scan_step`

## Scratch load evidence (2026-08-12)

```text
python -m spiderfeet_v2.db.bootstrap --database spiderfeet-spec017-a1 --reset
# applied_schema: true, errors: []
```

## spiderfeet-actual reload

Do **not** silent `--reset` on `spiderfeet-actual` (G1). Prefer:

1. Apply additive `define` for new attributes + `plays` / `owns` in a schema write transaction, **or**
2. Operator-approved G1 reset + full bootstrap when additive redefine is insufficient.

Existing data with singleton uuid5 temporary subgraphs remains until A4 reset path migrates/wipes multi-row temps.
