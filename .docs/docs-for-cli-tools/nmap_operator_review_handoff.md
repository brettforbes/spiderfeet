# Nmap Operator Review Handoff

## Scope

- Tool: `nmap`
- Issue: `#835`
- Refresh completed: 2026-06-25
- Source manifest: `.seed/scripts/cli_corpus/manifests/nmap.yaml`

## Evidence Refresh

- Ran `python .seed/scripts/cli_corpus/harvest.py --tool nmap`.
- Result: 30/30 manifest runs exited `0`.
- Evidence layout: `.docs/docs-for-cli-tools/app_examination_docs/nmap/`.
- Current legacy evidence count: 60 manifests and 60 review status files.

## Graph Regeneration

- Ran `python .seed/scripts/cli_corpus/nmap_xml_to_graph.py --all`.
- Generated 15 latest-per-scenario graph JSON files:
  - `.docs/docs-for-cli-tools/nugget_structure/nmap_*_proposed_nuggets_edges.json`
- Generated 15 latest-per-scenario semantic description files:
  - `.docs/docs-for-cli-tools/nugget_structure/nmap_*_proposed_nuggets_edges_description.md`
- Updated generator behavior to select the latest XML capture per scenario when legacy numbered runs contain duplicate scenario keys.

## Spot Checks

- `nse_default_permissive`: 42 nodes, 48 edges, description markdown present.
- `capstone_permissive`: 113 nodes, 130 edges, description markdown present.

## Verification

- `python -m pytest .tests/test_nmap_xml_to_graph.py` passed: 3 tests.
- `python -m py_compile .seed/scripts/cli_corpus/nmap_xml_to_graph.py .seed/scripts/cli_corpus/harvest.py spiderfeet/api/services/cli_corpus.py spiderfeet/api/routes/cli_corpus.py .tests/api/test_cli_corpus.py .tests/test_nmap_xml_to_graph.py` passed.
- `python -m pytest .tests/api/test_cli_corpus.py` blocked in this shell because `fastapi` is not installed.

## Review Notes

- Review the refreshed scenarios in the widget CLI Profiling tab.
- Start with `nse_default_permissive` and `capstone_permissive`; both exercise richer service/NSE output and generated description markdown.
- Scenario review statuses are initialized as `pending` in the generated `*_review.status.json` files.
