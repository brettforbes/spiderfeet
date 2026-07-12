# SPEC-006 structure doc gap inventory

**Date:** 2026-07-13  
**Quality bar:** `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md`  
**Gold reference:** `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`  
**Requirement:** R6-01-01

Scores use Q1–Q13 from the quality bar: **Pass**, **Fail**, **Missing**, or **N/A**.

## Summary

| Tool | Structure doc | Overall vs Nmap bar | Engine pack |
|------|---------------|----------------------|-------------|
| nmap | present (gold) | **Gold** | `rules/nmap/structure.yaml` |
| netdiscover | present (strong) | **Near gold** | `rules/netdiscover/structure.yaml` |
| nerva | present (thin) | **Rewrite** → engine | `rules/nerva/structure.yaml` |
| pius | present (thin) | **Rewrite** → engine | `rules/pius/structure.yaml` |
| subfinder | present (thin) | **Rewrite** → engine | `rules/subfinder/structure.yaml` |
| httpx | present (thin) | **Rewrite** → engine | `rules/httpx/structure.yaml` |
| katana | **was missing** | **Create** → engine | `rules/katana/structure.yaml` |
| nuclei | **was missing** | **Create** → engine | `rules/nuclei/structure.yaml` |

## Per-tool quality matrix (pre-engine baseline)

### nmap — Gold

| Q | Requirement | Pre-engine | Post-engine |
|---|-------------|------------|-------------|
| Q1 | Title | Pass | Pass |
| Q2 | Header | Pass | Pass |
| Q3 | Scan head + Mermaid | Pass | Pass |
| Q4 | Primary tree | Pass | Pass |
| Q5 | Specialty trees | Pass | Pass |
| Q6 | Scenario table | Pass | Pass |
| Q7 | Field mapping | Pass | Pass |
| Q8 | Nugget table | Pass | Pass |
| Q9 | Review notes | Pass | Pass |
| Q10 | Cross-link | Pass | Pass |
| Q11 | Mermaid purity | Pass | Pass |
| Q12 | Depth vs evidence | Pass | Pass |
| Q13 | Engine-owned | Fail (hand MD) | Pass |

**Live topology patterns (sample graphs):** `scan_head`, `host_status`, `host_networks_port_service`, `os_environment`, `ssh_host_keys`, `trace_hop_chain`.

### netdiscover — Near gold

| Q | Pre-engine | Post-engine |
|---|------------|-------------|
| Q1–Q12 | Pass | Pass |
| Q13 | Fail | Pass |

**Live patterns:** `scan_head`, `system_l2`, multi-`SYSTEM` per scan.

### nerva — Thin (rewrite)

| Q | Pre-engine | Gap |
|---|------------|-----|
| Q3–Q5 | Partial | Single shallow service Mermaid; missing CDN branch, APPLICATIONS category alignment |
| Q6 | Partial | Output-class table only; not full manifest scenario keys |
| Q7 | Missing | No field mapping table |
| Q8 | Missing | No proposed nuggets table |
| Q9 | Partial | Minimal review notes |
| Q10 | Missing | No `_Current_Ontology.md` link |
| Q13 | Fail | Hand-maintained |

**Live patterns (adapters/nerva/hooks.py):** `scan_head`, `host_networks_port_service`, CDN reclassification, SERVICE descriptors, misconfig facts.

### pius — Thin (rewrite)

| Q | Pre-engine | Gap |
|---|------------|-----|
| Q4–Q5 | Partial | Findings table only; no org category Mermaid |
| Q6 | Partial | Scenario list incomplete vs manifest |
| Q7 | Partial | NDJSON Type table only |
| Q8 | Missing | No proposed nuggets |
| Q10 | Missing | No ontology cross-link |
| Q13 | Fail | Hand-maintained |

**Live patterns:** `scan_head`, `org_company_tree` (`COMPANY_NAME` → `DOMAINS`/`NETBLOCKS`).

### subfinder — Thin (rewrite)

| Q | Pre-engine | Gap |
|---|------------|-----|
| Q1 | Fail | Title missing em-dash contract |
| Q3–Q5 | Fail | Bullet lists; no Mermaid |
| Q7 | Partial | Inline table only |
| Q8–Q9 | Partial | Notes embedded in bullets |
| Q10 | Missing | No cross-link |
| Q13 | Fail | Hand-maintained |

**Live patterns:** `scan_head`, `domain_apex`, passive vs active IP attachment.

### httpx — Thin (rewrite)

| Q | Pre-engine | Gap |
|---|------------|-----|
| Q1 | Fail | Title format |
| Q3–Q5 | Fail | Pipeline bullets; no Mermaid |
| Q6 | Pass | Scenario table present |
| Q7 | Partial | Per-field table without structured paths |
| Q10 | Missing | No cross-link |
| Q13 | Fail | Hand-maintained |

**Live patterns:** `scan_head`, `web_url_probe`, HOST/CDN + NETWORKS + APPLICATIONS.

### katana — Missing (create)

| Q | Pre-engine | Gap |
|---|------------|-----|
| All Q1–Q12 | **Missing** | No `katana_nugget_graph_structure.md` on disk |
| Q13 | N/A | No pack before SPEC-006 |

**Live patterns (adapters/katana/hooks.py):** `scan_head`, `crawl_url_tree`, `DOMAIN_NAME` + `LINKED_URL_INTERNAL`.

### nuclei — Missing (create)

| Q | Pre-engine | Gap |
|---|------------|-----|
| All Q1–Q12 | **Missing** | No `nuclei_nugget_graph_structure.md` on disk |
| Q13 | N/A | No pack before SPEC-006 |

**Live patterns (adapters/nuclei/hooks.py):** `scan_head`, `vuln_findings`, `SECURITY` → `FINDINGS` → severity → `NUCLEI_FINDING`.

## Remediation status

After `render_structure_docs.py --all` and `--ontology`:

- All eight ADAPTER_TOOLS have engine-owned `rules/<tool>/structure.yaml`.
- All eight `*_nugget_graph_structure.md` files regenerate from YAML.
- `_Current_Ontology.md` composes sub-graph table + per-tool sections from packs.
- Governance tests: `.tests/test_structure_doc_engine.py`, `.tests/test_spec006_structure_docs.py`.

## Verification

```bash
poetry run python .seed/scripts/cli_corpus/render_structure_docs.py --all
poetry run python .seed/scripts/cli_corpus/render_structure_docs.py --ontology
poetry run pytest .tests/test_structure_doc_engine.py .tests/test_spec006_structure_docs.py -q
```
