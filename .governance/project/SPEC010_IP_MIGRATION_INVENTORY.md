# SPEC-010 — IP_ADDRESS migration inventory (AH0)

**Date:** 2026-08-07
**Issue:** [#1066](https://github.com/brettforbes/spiderfeet/issues/1066) (AH0)
**Requirement:** R10-01
**Goal:** Split ambiguous `IP_ADDRESS` -> `IPV4_ADDRESS` / `IPV6_ADDRESS` across the canonical CLI-profiling stack.

## Summary

| Classification | Files | Matches |
|---------------|------:|--------:|
| `migrate` | 56 | 135 |
| `regen-artifact` | 73 | 2391 |
| `keep-legacy` | 618 | 1431 |
| **Total (`rg IP_ADDRESS`)** | **747** | **3957** |

### Verification command

```bash
rg -c --hidden IP_ADDRESS --glob "!.git/**" --glob "!**/__pycache__/**" --glob "!**/.venv/**" --glob "!**/node_modules/**" --glob "!**/dist/**" --glob "!**/.codegraph/**" --glob "!**/.cursor/**" --glob "!**/agent-transcripts/**" --glob "!**/SPEC010_IP_MIGRATION_INVENTORY.md" --glob "!**/_gen_ip_migration_inventory.py"
# Expected: files and match counts equal the Total row above.
```

- Inventory total matches: **3957**
- Inventory total files: **747**

## Central classifier status (`core/ip_classify.py`)

`classify_ip()` already routes literals through `rules/_shared/ip_patterns.yaml` roles.

| Role | Current IPv4 mapping | Current IPv6 mapping | AH target IPv4 | AH target IPv6 |
|------|----------------------|----------------------|----------------|----------------|
| host | `IP_ADDRESS` | `IPV6_ADDRESS` | **`IPV4_ADDRESS`** | `IPV6_ADDRESS` |
| internal | `INTERNAL_IP_ADDRESS` | `IPV6_ADDRESS` | keep (or later `INTERNAL_IPV4_ADDRESS`) | keep / follow-up |
| affiliate | `AFFILIATE_IPADDR` | `AFFILIATE_IPV6_ADDRESS` | keep (v1 event name) or follow-up split | keep |

- Confirmed host IPv4 currently maps to `IP_ADDRESS`: **True**
- Confirmed host IPv6 currently maps to `IPV6_ADDRESS`: **True**
- Decision (operator): host IPv4 becomes `IPV4_ADDRESS`; host IPv6 stays `IPV6_ADDRESS`.

## Catalogue status

| nugget_id | In `nuggets.json` | In `nuggets_extension.json` | AH action |
|-----------|:-----------------:|:---------------------------:|-----------|
| `IP_ADDRESS` | yes | no | retire from emitting code; retain in nuggets.json as keep-legacy v1 event type until v1 sunset |
| `IPV4_ADDRESS` | no | no | **ADD** to nuggets_extension.json (AH1) |
| `IPV6_ADDRESS` | yes | no | already present in nuggets.json — reuse |
| `INTERNAL_IP_ADDRESS` | yes | no | keep (IPv4-internal); note ambiguity vs IPV4 — follow-up if needed |
| `AFFILIATE_IPADDR` | yes | no | keep-legacy v1 event name (not host classifier role for v2 graphs) |
| `AFFILIATE_IPV6_ADDRESS` | yes | no | keep |
| `BLACKLISTED_IPADDR` | yes | no | keep-legacy v1 |
| `BLACKLISTED_AFFILIATE_IPADDR` | yes | no | keep-legacy v1 |
| `MALICIOUS_IPADDR` | yes | no | keep-legacy v1 |
| `MALICIOUS_AFFILIATE_IPADDR` | yes | no | keep-legacy v1 |

## `migrate` — must change in AH1–AH3

### A. cli_corpus (code + rules) (32 matches / 16 files)

| Matches | Path |
|--------:|------|
| 5 | `.seed/scripts/cli_corpus/narrative_report.py` |
| 5 | `.seed/scripts/cli_corpus/rules/_shared/structure_v1.yaml` |
| 4 | `.seed/scripts/cli_corpus/rules/subfinder/structure.yaml` |
| 2 | `.seed/scripts/cli_corpus/ONBOARDING.md` |
| 2 | `.seed/scripts/cli_corpus/nmap_xml_to_graph.py` |
| 2 | `.seed/scripts/cli_corpus/rules/_shared/ip_patterns.yaml` |
| 2 | `.seed/scripts/cli_corpus/rules/_shared/topology_templates.yaml` |
| 2 | `.seed/scripts/cli_corpus/rules/nmap/structure.yaml` |
| 1 | `.seed/scripts/cli_corpus/adapters/httpx/hooks.py` |
| 1 | `.seed/scripts/cli_corpus/adapters/nmap/hooks.py` |
| 1 | `.seed/scripts/cli_corpus/core/structure_doc_engine.py` |
| 1 | `.seed/scripts/cli_corpus/rules/_template/mapping.yaml` |
| 1 | `.seed/scripts/cli_corpus/rules/httpx/structure.yaml` |
| 1 | `.seed/scripts/cli_corpus/rules/nerva/structure.yaml` |
| 1 | `.seed/scripts/cli_corpus/rules/netdiscover/structure.yaml` |
| 1 | `.seed/scripts/cli_corpus/rules/subfinder/narrative.yaml` |

### B. catalogues (.docs/analysis) (5 matches / 3 files)

| Matches | Path |
|--------:|------|
| 2 | `.docs/analysis/nuggets.json` |
| 2 | `.docs/analysis/nuggets_id_type.csv` |
| 1 | `.docs/analysis/nuggets_consumed_list.json` |

### C. tool structure docs (26 matches / 6 files)

| Matches | Path |
|--------:|------|
| 7 | `.docs/docs-for-cli-tools/_Current_Ontology.md` |
| 6 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_nugget_graph_structure.md` |
| 4 | `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md` |
| 3 | `.docs/docs-for-cli-tools/nugget_structure/httpx_nugget_graph_structure.md` |
| 3 | `.docs/docs-for-cli-tools/nugget_structure/nerva_nugget_graph_structure.md` |
| 3 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_nugget_graph_structure.md` |

### D. CLI tool guides (Zero-to-Hero / options) (18 matches / 15 files)

| Matches | Path |
|--------:|------|
| 3 | `.docs/docs-for-cli-tools/NMAP-Zero-to-Hero.md` |
| 2 | `.docs/docs-for-cli-tools/TextFMS-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/Httpx-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/NTLMRecon-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/Nerva-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/NetDiscover-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/SubFinder-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/TextFSM-Templates-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/dnsx-CLI-Options.md` |
| 1 | `.docs/docs-for-cli-tools/dnsx-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/examination_plans/nmap_exploration_report.md` |
| 1 | `.docs/docs-for-cli-tools/mapcidr-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/recon-ng-Zero-to-Hero.md` |
| 1 | `.docs/docs-for-cli-tools/uncover-Zero-to-Hero.md` |

### E. modules_v2 content + stubs (28 matches / 11 files)

| Matches | Path |
|--------:|------|
| 6 | `modules_v2/content/subfinder/graph_structure.md` |
| 4 | `modules_v2/content/nmap/graph_structure.md` |
| 3 | `modules_v2/content/httpx/graph_structure.md` |
| 3 | `modules_v2/content/nerva/graph_structure.md` |
| 3 | `modules_v2/content/netdiscover/graph_structure.md` |
| 3 | `modules_v2/content/nmap/zero_to_hero.md` |
| 2 | `modules_v2/sfp_cli_nmap.py` |
| 1 | `modules_v2/content/httpx/zero_to_hero.md` |
| 1 | `modules_v2/content/nerva/zero_to_hero.md` |
| 1 | `modules_v2/content/netdiscover/zero_to_hero.md` |
| 1 | `modules_v2/content/subfinder/zero_to_hero.md` |

### F. v2 TypeDB schema (2 matches / 1 files)

| Matches | Path |
|--------:|------|
| 2 | `.seed/spiderfeet_v2_semantic.tql` |

### H. governance / SPEC docs (24 matches / 4 files)

| Matches | Path |
|--------:|------|
| 12 | `.governance/project/SPEC010_AGENT_PLAN.md` |
| 7 | `.governance/specs/SPEC-010-spiderfeet-v2-engine.md` |
| 4 | `.governance/project/SPEC005_AGENT_PLAN.md` |
| 1 | `.governance/specs/SPEC-005-narrative-v2-ip-classify.md` |

## `regen-artifact` — regenerate in AH4 (do not hand-edit)

**2391 matches in 73 files** — graph JSON + narrative MD under `.docs/docs-for-cli-tools/nugget_structure/` (and exploration scratch).

Regenerate via:

```bash
poetry run python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool <tool>
# for each of: nmap netdiscover nerva pius subfinder httpx katana nuclei
```

Also refresh `modules_v2/content/<tool>/graph_structure.md` from the structure docs.

<details><summary>Full regen-artifact file list</summary>

| Matches | Path |
|--------:|------|
| 800 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_sbs_proposed_nuggets_edges.json` |
| 528 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_sbs_proposed_nuggets_edges_description.md` |
| 69 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_squarepeg_proposed_nuggets_edges.json` |
| 63 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_upside_com_proposed_nuggets_edges.json` |
| 51 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_squarepeg_proposed_nuggets_edges_description.md` |
| 49 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_upside_com_proposed_nuggets_edges_description.md` |
| 48 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_active_parsable_proposed_nuggets_edges.json` |
| 48 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_active_text_proposed_nuggets_edges.json` |
| 48 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_passive_snippet_text_proposed_nuggets_edges.json` |
| 48 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_sparse_subnet_parsable_proposed_nuggets_edges.json` |
| 35 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_k2am_passive_proposed_nuggets_edges.json` |
| 34 | `.docs/docs-for-cli-tools/nugget_structure/nmap_capstone_permissive_proposed_nuggets_edges.json` |
| 34 | `.docs/docs-for-cli-tools/nugget_structure/nmap_os_aggressive_permissive_proposed_nuggets_edges.json` |
| 33 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_k2am_active_proposed_nuggets_edges.json` |
| 33 | `.docs/docs-for-cli-tools/nugget_structure/nmap_traceroute_permissive_proposed_nuggets_edges.json` |
| 29 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_k2am_passive_proposed_nuggets_edges_description.md` |
| 27 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_k2am_active_proposed_nuggets_edges_description.md` |
| 26 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_k2am_active_oI_proposed_nuggets_edges.json` |
| 24 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_upside_au_proposed_nuggets_edges.json` |
| 24 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_active_parsable_proposed_nuggets_edges_description.md` |
| 24 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_active_text_proposed_nuggets_edges_description.md` |
| 24 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_passive_snippet_text_proposed_nuggets_edges_description.md` |
| 24 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_sparse_subnet_parsable_proposed_nuggets_edges_description.md` |
| 20 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_upside_au_proposed_nuggets_edges_description.md` |
| 19 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_k2am_active_oI_proposed_nuggets_edges_description.md` |
| 17 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_vcof_sparse_proposed_nuggets_edges.json` |
| 16 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_list_file_json_proposed_nuggets_edges.json` |
| 15 | `.docs/docs-for-cli-tools/nugget_structure/httpx_from_subfinder_vcof_sparse_proposed_nuggets_edges_description.md` |
| 12 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_list_file_json_proposed_nuggets_edges_description.md` |
| 10 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_fast_praetorian_json_proposed_nuggets_edges.json` |
| 10 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_https_praetorian_json_proposed_nuggets_edges.json` |
| 10 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_local_proposed_nuggets_edges.json` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_fast_praetorian_json_proposed_nuggets_edges_description.md` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_https_praetorian_json_proposed_nuggets_edges_description.md` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nmap_capstone_permissive_proposed_nuggets_edges_description.md` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_local_subnet_proposed_nuggets_edges.json` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nmap_os_aggressive_permissive_proposed_nuggets_edges_description.md` |
| 8 | `.docs/docs-for-cli-tools/nugget_structure/nmap_traceroute_permissive_proposed_nuggets_edges_description.md` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_http_rich_json_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_http_rich_json_proposed_nuggets_edges_description.md` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_ssh_misconfigs_json_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nerva_tcp_ssh_misconfigs_json_proposed_nuggets_edges_description.md` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_nse_default_permissive_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_service_version_corporate_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_service_version_permissive_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_skip_ping_permissive_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_corporate_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json` |
| 5 | `.docs/docs-for-cli-tools/nugget_structure/nmap_udp_top_permissive_proposed_nuggets_edges.json` |
| 4 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_fast_parsable_proposed_nuggets_edges.json` |
| 4 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_corporate_proposed_nuggets_edges.json` |
| 4 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_permissive_proposed_nuggets_edges.json` |
| 2 | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_fast_parsable_proposed_nuggets_edges_description.md` |
| 2 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_local_subnet_proposed_nuggets_edges_description.md` |
| 2 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_local_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/exploration_scratch/subfinder/org_size_matrix/exploration_report.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_corporate_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_host_discovery_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_nse_default_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_proposed_nuggets.json` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_service_version_corporate_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_service_version_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_skip_ping_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_corporate_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/nmap_udp_top_permissive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_k2am_passive_cs_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_squarepeg_passive_cs_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_upside_com_passive_cs_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_vcof_sparse_passive_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_enterprise_sbs_passive_cs_proposed_nuggets_edges_description.md` |
| 1 | `.docs/docs-for-cli-tools/nugget_structure/subfinder_invalid_domain_clean_miss_proposed_nuggets_edges_description.md` |

</details>

## `keep-legacy` — out of AH emitting-path scope

| Top-level | Files | Matches | Rationale |
|-----------|------:|--------:|-----------|
| `.docs/` | 215 | 716 | non-canonical docs outside migrate buckets |
| `test/` | 245 | 284 | v1 unit/integration tests bound to v1 event names |
| `modules/` | 94 | 253 | v1 OSINT `sfp_*` event types — SPEC-010 forbids touching these |
| `.seed/` | 25 | 109 | historic issue-generator scripts / unrelated seeds |
| `.tests/` | 20 | 38 | legacy / out of AH emitting scope |
| `spiderfeet/` | 6 | 13 | v1 package (target typing, map seeds, API schemas) — keep until v1 sunset |
| `.governance/` | 8 | 11 | historic SPEC text mentioning IP_ADDRESS as example |
| `correlations/` | 3 | 4 | v1 correlation YAML using IP_ADDRESS event names |
| `.references/` | 1 | 2 | legacy / out of AH emitting scope |
| `.strategy/` | 1 | 1 | legacy / out of AH emitting scope |

Total keep-legacy: **1431** matches in **618** files.

## Derived `*_IPADDR` audit (not host-role rename)

| Variant | Matches | Files | AH decision |
|---------|--------:|------:|-------------|
| `AFFILIATE_IPADDR` | 706 | 171 | keep-legacy (v1 event); affiliate role stays AFFILIATE_IPADDR for IPv4 until a later split |
| `BLACKLISTED_IPADDR` | 187 | 105 | keep-legacy v1 |
| `MALICIOUS_IPADDR` | 295 | 167 | keep-legacy v1 |
| `INTERNAL_IP_ADDRESS` | 38 | 31 | keep for now (internal IPv4); optional follow-up to INTERNAL_IPV4_ADDRESS |
| `AFFILIATE_IPV6_ADDRESS` | 124 | 75 | keep |
| `IPV6_ADDRESS` | 479 | 160 | keep / already correct for host IPv6 |
| `IPV4_ADDRESS` | 15 | 3 | add to catalogue (AH1); currently sparse (governance/plan mentions only) |

## AH story mapping

| Story | Action |
|-------|--------|
| **AH1** | Add `IPV4_ADDRESS` (+ confirm `IPV6_ADDRESS`) to `nuggets_extension.json`; document derived-variant decisions |
| **AH2** | Change `ip_patterns.yaml` host.ipv4 → `IPV4_ADDRESS`; update rules/adapters/topology so emitters use `classify_ip` only |
| **AH3** | Align `spiderfeet_v2_semantic.tql` comments; update structure docs, `_Current_Ontology.md`, proj-07 IP table |
| **AH4** | Backfill all 8 tools; refresh content `graph_structure.md`; prove no non-legacy `IP_ADDRESS` in migrate+regen surfaces |

## Exit criteria for AH0

- [x] Every `IP_ADDRESS` occurrence classified `migrate` / `regen-artifact` / `keep-legacy`
- [x] `classify_ip` confirmed as single source of truth for address literals
- [x] Grep totals recorded for verification against a fresh `rg -c IP_ADDRESS`
