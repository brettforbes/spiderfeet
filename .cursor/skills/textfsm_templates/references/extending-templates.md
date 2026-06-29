# Extending NTC Templates for OSINT CLI Output

## When to extend

| Situation | Action |
|-----------|--------|
| Stock NTC template matches | Use bundled `template_dir=None` |
| OSINT CLI text output | Add project-local template + index row |
| Same tool, two output modes | Two templates + two index rows |
| Output is JSON/XML | **Do not** use NTC — native parser |

## Authoring workflow

1. **Capture fixture** — `{scenario}_output_text.txt` from formal examination.
2. **Identify rows** — tabular lines, key columns, banners to skip.
3. **Draft `.textfsm`** — follow [`textfsm-syntax-primer.md`](textfsm-syntax-primer.md) and [`../../textfsm/references/template-syntax.md`](../../textfsm/references/template-syntax.md).
4. **Validate locally**:

```bash
python -m textfsm.parser path/to/template.textfsm path/to/fixture.txt
```

5. **Add index row** — see [platform-index.md](platform-index.md).
6. **Wire `parse_output`** — confirm `list[dict]` matches expected keys.
7. **Map nuggets** — [nugget-conversion.md](nugget-conversion.md).
8. **Optional upstream PR** — contribute generic templates to networktocode/ntc-templates if broadly reusable.

## Project layout (recommended)

```
.docs/docs-for-cli-tools/textfsm_templates/
  index
  spiderfeet_netdiscover_parsable.textfsm
  spiderfeet_netdiscover_active.textfsm
  README.md
```

Keep templates **next to** the tool corpus under `.docs/docs-for-cli-tools/` for traceability.

## Template naming convention

```
spiderfeet_{tool}_{scenario_or_mode}.textfsm
```

Examples:

- `spiderfeet_netdiscover_parsable.textfsm`
- `spiderfeet_naabu_default.textfsm`

## Development checklist (from NTC dev guide)

- [ ] Template parses fixture without hitting `Error` state
- [ ] All required nugget fields captured as `Value` columns
- [ ] `List` used for multi-value cells (interfaces, ports list)
- [ ] `Filldown` for hostname/context lines
- [ ] Index row Platform + Command tested via `parse_output`
- [ ] Parser function + unit test with fixture text
- [ ] `to_nodes_edges()` validated against approved `proposed_nuggets_edges.json`

## Contributing upstream

Follow https://ntc-templates.readthedocs.io/en/latest/dev/contributing/:

- Fork networktocode/ntc-templates
- Add template under `ntc_templates/templates/`
- Update platform index
- Include parsed example in tests
- OSINT-specific templates may stay **SpiderFeet-local** unless accepted upstream

## Version upgrades

See https://ntc-templates.readthedocs.io/en/latest/admin/upgrade/

After upgrade, re-run corpus fixtures — template column renames can break parsers.
