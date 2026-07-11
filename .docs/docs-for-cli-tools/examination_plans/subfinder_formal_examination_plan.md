# Subfinder — formal examination plan (v1)

**Tool:** ProjectDiscovery Subfinder v2.6.8  
**Structured family:** JSONL (`-oJ`) → harvest bundle `subfinder_host_v1` with `records[]`  
**Exploration basis:** `.docs/docs-for-cli-tools/exploration_scratch/subfinder/org_size_matrix/exploration_report.md`

## Semantic outcome matrix

| Row | Scenario id | Target class | Expected shape |
|-----|-------------|--------------|----------------|
| Rich SME passive | `corporate_upside_au_passive_cs` | Medium org | Many hosts, `sources[]` array, no `ip` |
| Small VC passive | `corporate_squarepeg_passive_cs` | Small org | Few hosts, campaign/data subs |
| Ultra-sparse | `corporate_vcof_sparse_passive` | Near clean-miss | `records: []` or single `www` row |
| Medium hosting | `corporate_k2am_passive_cs` | SME | cpanel/mail/owa pattern |
| Active + IP | `corporate_k2am_active_oI` | SME | `source` string + `ip` field |
| TLD sibling | `corporate_upside_com_passive_cs` | Related zone | Sparser than `.com.au` |
| Enterprise | `enterprise_sbs_passive_cs` | Large org | High volume, deep labels |
| Clean miss | `invalid_domain_clean_miss` | Invalid apex | Empty `records[]`, exit 0 |

## Examination slots

| # | Scenario | Priority |
|---|----------|----------|
| 1 | `corporate_upside_au_passive_cs` | P0 |
| 2 | `corporate_squarepeg_passive_cs` | P0 |
| 3 | `corporate_vcof_sparse_passive` | P0 |
| 4 | `corporate_k2am_passive_cs` | P1 |
| 5 | `corporate_k2am_active_oI` | P1 |
| 6 | `corporate_upside_com_passive_cs` | P1 |
| 7 | `enterprise_sbs_passive_cs` | P2 |
| 8 | `invalid_domain_clean_miss` | P2 |

## Harvest

```bash
python .seed/scripts/cli_corpus/harvest.py --tool subfinder
```

## Graph mapping

See `.cursor/skills/subfinder/references/nugget-mapping.md` and `subfinder_json_to_graph.py`.
