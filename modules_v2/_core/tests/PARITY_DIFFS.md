# AJ4 parity harness — explained diffs (R10-12)

Harness: `modules_v2/_core/tests/test_parity.py`

## Mode

Adapters / hooks remain under `.seed/scripts/cli_corpus/adapters/` until Epic AK.
This harness therefore proves **ported `_core` + `_rules` parity** (RuleEngine, topology,
narrative, IP classify, catalogues) against recorded corpus goldens — not a full
`adapters.<tool>.build_outputs` re-run inside `modules_v2/`.

Production `modules_v2/` code does **not** import `cli_corpus`. The optional
side-by-side RuleEngine check loads original `core` only via a one-shot subprocess
for comparison evidence.

## Per-tool fixture + expectation

| Tool | Fixture (structured) | Golden graph / MD | Ported path | Expectation |
|------|----------------------|-------------------|-------------|-------------|
| netdiscover | `app_examination_docs/netdiscover/3_output_structured.json` (`local_subnet_fast_parsable`) | matching nugget_structure pair | `topology.add_scan_head` + `add_system_l2` (mirrors adapter) | Near full graph parity (node count ±2, nugget_id sets equal) |
| nerva | `…/nerva/6_output_structured.json` (`tcp_closed_clean_miss`) | matching pair | RuleEngine + `SCAN_TOOL` | Near full parity (empty `records[]`; no hook host tree) |
| katana | `…/katana/3_output_structured.json` (`from_httpx_vcof_sparse`) | matching pair | RuleEngine + `SCAN_TOOL` + target/`httpx_scenario` descriptors | Near full parity (empty crawl; minimal hook surface) |
| nmap | synthetic `tests/fixtures/nmap_scan_head.json` + golden `host_discovery_permissive_xml` for narrative | RuleEngine scan-head only; narrative re-render on golden | Scan-head subset; host/port tree needs `apply_nmap_hosts` (AK0) |
| pius | `…/pius/4_output_structured.json` (`corporate_squarepeg_ndjson`) | matching pair | RuleEngine + `SCAN_TOOL` | Scan-head subset; org/domain tree needs `apply_pius_records` (AK3) |
| subfinder | `…/subfinder/3_output_structured.json` (`corporate_vcof_sparse_passive`) | matching pair | RuleEngine + `SCAN_TOOL` | Scan-head subset; host tree needs `apply_subfinder_records` (AK4) |
| httpx | `…/httpx/3_output_structured.json` (`from_subfinder_vcof_sparse`) | matching pair | RuleEngine + `SCAN_TOOL` | Scan-head subset; host/HTTP tree needs `apply_httpx_records` (AK5) |
| nuclei | `…/nuclei/3_output_structured.json` (`cipherheart_redis_lab`) | matching pair | RuleEngine + `SCAN_TOOL` | Scan-head subset; finding tree needs `apply_nuclei_records` (AK7) |

## Explained diffs (acceptable)

1. **Adapter hooks not ported** — rich host/finding trees on pius/subfinder/httpx/nuclei/nmap
   goldens exceed RuleEngine scan-head graphs. Asserted as: ported nugget_id set ⊆ golden
   after normalize; node-count tolerance applies only to near-full tools.
2. **`SCAN_START` formatting (nerva)** — some goldens store a locale-formatted start time
   while structured fixtures keep ISO `started_at`. RuleEngine emits the structured value;
   nugget_id set still matches; instance ids for `SCAN_START` may differ.
3. **Narrative re-render** — `render_narrative(golden_graph)` via `modules_v2._core` must be
   non-empty and cover nodes; byte-equality with on-disk MD is not required (intro phrasing /
   section order may drift with shared `narrative_v2.yaml`).
4. **AH IPv4/IPv6** — normalized graphs must contain **no** `IP_ADDRESS` nodes; address nodes
   are `IPV4_ADDRESS` / `IPV6_ADDRESS` (or affiliate/internal variants).

## Gaps closed by later issues

| Gap | Follow-up |
|-----|-----------|
| Full adapter `build_outputs` inside `modules_v2` | AK0–AK7 (`sfp_cli_<tool>.py`) |
| Byte-equal narrative MD vs corpus | Optional after AK + visual review |
