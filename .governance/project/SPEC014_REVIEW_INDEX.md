# SPEC-014 narrative review index (BF1)

**Issue:** #1189 · **Requirement:** R14-09 · **PR:** (this PR)

All scenario Markdown under `.docs/docs-for-cli-tools/nugget_structure/*_proposed_nuggets_edges_description.md`
was regenerated with `backfill_adapter_four_outputs.py --force` through the shared meta-concept engine.

## Operator visual review gate

Please review a sample of reports in CLI Profiling (Report / Markdown tab) and comment approval on #1189.
**Do not start BG1** until this index is approved.

Suggested spot-checks:
- `pius_corporate_upside_ndjson` — org + domains with capped example Mermaids
- `nmap_tcp_top_ports_permissive` — host networks/applications progressive disclosure
- `netdiscover_local_subnet_active_parsable` — system + NETWORKS
- `nuclei_pg_dvwa_tech_fingerprint` — security findings
- `subfinder_corporate_k2am_active_oI` — domains

**Validator summary:** failures=0

## httpx (8 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `from_subfinder_invalid_clean_miss` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_k2am_active` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_k2am_passive` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_sbs` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_squarepeg` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_upside_au` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_upside_com` | OK | progressive disclosure + deduped appendix |
| `from_subfinder_vcof_sparse` | OK | progressive disclosure + deduped appendix |

## katana (2 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `from_httpx_upside_com` | OK | progressive disclosure + deduped appendix |
| `from_httpx_vcof_sparse` | OK | progressive disclosure + deduped appendix |

## nerva (6 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `tcp_closed_clean_miss` | OK | progressive disclosure + deduped appendix |
| `tcp_fast_praetorian_json` | OK | progressive disclosure + deduped appendix |
| `tcp_http_rich_json` | OK | progressive disclosure + deduped appendix |
| `tcp_https_praetorian_json` | OK | progressive disclosure + deduped appendix |
| `tcp_list_file_json` | OK | progressive disclosure + deduped appendix |
| `tcp_ssh_misconfigs_json` | OK | progressive disclosure + deduped appendix |

## netdiscover (5 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `local_subnet_active_parsable` | OK | progressive disclosure + deduped appendix |
| `local_subnet_active_text` | OK | progressive disclosure + deduped appendix |
| `local_subnet_fast_parsable` | OK | progressive disclosure + deduped appendix |
| `passive_snippet_text` | OK | progressive disclosure + deduped appendix |
| `sparse_subnet_parsable` | OK | progressive disclosure + deduped appendix |

## nmap (30 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `capstone_permissive` | OK | progressive disclosure + deduped appendix |
| `capstone_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `host_discovery_corporate` | OK | progressive disclosure + deduped appendix |
| `host_discovery_corporate_xml` | OK | progressive disclosure + deduped appendix |
| `host_discovery_local_subnet` | OK | progressive disclosure + deduped appendix |
| `host_discovery_local_subnet_xml` | OK | progressive disclosure + deduped appendix |
| `host_discovery_permissive` | OK | progressive disclosure + deduped appendix |
| `host_discovery_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `nse_default_permissive` | OK | progressive disclosure + deduped appendix |
| `nse_default_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `os_aggressive_permissive` | OK | progressive disclosure + deduped appendix |
| `os_aggressive_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `service_version_corporate` | OK | progressive disclosure + deduped appendix |
| `service_version_corporate_xml` | OK | progressive disclosure + deduped appendix |
| `service_version_permissive` | OK | progressive disclosure + deduped appendix |
| `service_version_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `skip_ping_permissive` | OK | progressive disclosure + deduped appendix |
| `skip_ping_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_corporate` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_corporate_xml` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_local` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_local_xml` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_permissive` | OK | progressive disclosure + deduped appendix |
| `tcp_top_ports_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `traceroute_permissive` | OK | progressive disclosure + deduped appendix |
| `traceroute_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `udp_top_permissive` | OK | progressive disclosure + deduped appendix |
| `udp_top_permissive_xml` | OK | progressive disclosure + deduped appendix |
| `windows_enrich_local` | OK | progressive disclosure + deduped appendix |
| `windows_enrich_local_xml` | OK | progressive disclosure + deduped appendix |

## nuclei (5 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `cipherheart_redis_lab` | OK | progressive disclosure + deduped appendix |
| `pg_dvwa_tech_fingerprint` | OK | progressive disclosure + deduped appendix |
| `pg_graphql_graphql_misconfig` | OK | progressive disclosure + deduped appendix |
| `pg_shadowlogic_weblogic_cves` | OK | progressive disclosure + deduped appendix |
| `scanme_all_templates` | OK | progressive disclosure + deduped appendix |

## pius (6 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `corporate_bbc_gleif_ndjson` | OK | progressive disclosure + deduped appendix |
| `corporate_k2am_ndjson` | OK | progressive disclosure + deduped appendix |
| `corporate_squarepeg_ndjson` | OK | progressive disclosure + deduped appendix |
| `corporate_upside_ndjson` | OK | progressive disclosure + deduped appendix |
| `crt_linode_ndjson` | OK | progressive disclosure + deduped appendix |
| `crt_praetorian_ndjson` | OK | progressive disclosure + deduped appendix |

## subfinder (8 scenarios)

| Scenario | Status | Notes |
| --- | --- | --- |
| `corporate_k2am_active_oI` | OK | progressive disclosure + deduped appendix |
| `corporate_k2am_passive_cs` | OK | progressive disclosure + deduped appendix |
| `corporate_squarepeg_passive_cs` | OK | progressive disclosure + deduped appendix |
| `corporate_upside_au_passive_cs` | OK | progressive disclosure + deduped appendix |
| `corporate_upside_com_passive_cs` | OK | progressive disclosure + deduped appendix |
| `corporate_vcof_sparse_passive` | OK | progressive disclosure + deduped appendix |
| `enterprise_sbs_passive_cs` | OK | progressive disclosure + deduped appendix |
| `invalid_domain_clean_miss` | OK | progressive disclosure + deduped appendix |

## Totals

- Scenarios indexed: **70**
- Validator failures: **0**

---

*Generated by SPEC-014 BF1*
