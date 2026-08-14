# SPEC-018 A4 — Nuclei input contract proof

Evidence from corpus fixtures only (no live Nuclei run).

## Katana `crawl_urls` GSE (post-A2)

| Field | Value |
|-------|-------|
| Fixture | `.docs/docs-for-cli-tools/nugget_structure/katana_from_httpx_upside_com_proposed_nuggets_edges.json` |
| Count | 3411 |
| Empty? | no |
| Primary nuggets | `LINKED_URL_INTERNAL` (3370), `DOMAIN_NAME` (41) |
| Sample | `a.klaviyo.com`, `a.shgcdn2.com`, `apco.org.au` |

12A selector (`sfp_cli_katana.output.vars.crawl_urls`):

- `nugget_id_in`: `LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`, `DOMAIN_NAME`
- `project`: `nugget_data`, `distinct`: true

## Nuclei wiring (12A)

- **Input:** `$steps.sfp_cli_katana.vars.crawl_urls` with `empty: skip_step`
- **Argv:** `-l` → `$step.files.input` (line list), `-jsonl`, `-jle` → output
- **Timeout:** 900s unchanged — list is non-empty and proven; timeout is operational, not GSE-empty

## Conclusion

- Nuclei skip when Katana produces zero URLs is correct (`empty: skip_step`).
- On the upside.com corpus chain, Katana GSE yields a large but **non-empty** URL list.
- Live timeout after 900s with ~3k URLs is a wall-clock / template-scope issue (E1), not an empty GSE binding.

## Verification

`poetry run pytest spiderfeet_v2/workflow/tests/test_gse_12a_chain.py -q`
