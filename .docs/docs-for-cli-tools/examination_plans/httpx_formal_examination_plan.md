# httpx formal examination plan (v1)

**Tool:** ProjectDiscovery httpx v1.6.10  
**Input:** Host lists from subfinder formal examinations  
**Structured family:** JSONL (`-json`) → harvest bundle `httpx_probe_v1` with `records[]`

## Pipeline

```
subfinder examination → prepare_httpx_hosts_from_subfinder.py → hosts.txt → httpx -l -json -no-stdin
```

**Critical:** Always `-no-stdin` when not piping on Windows — otherwise httpx blocks waiting for stdin.

## Probe profile

`-status-code -title -tech-detect -server -cdn -ip -json -no-stdin -silent`

## Scenarios (mirror subfinder P0/P1/P2)

| # | httpx scenario | Subfinder source | Hosts in | Live URLs |
|---|----------------|------------------|----------|-----------|
| 1 | `from_subfinder_upside_au` | corporate_upside_au_passive_cs | 26 | varies |
| 2 | `from_subfinder_squarepeg` | corporate_squarepeg_passive_cs | 7 | 7 |
| 3 | `from_subfinder_vcof_sparse` | corporate_vcof_sparse_passive | 1 | 1 |
| 4 | `from_subfinder_k2am_passive` | corporate_k2am_passive_cs | 18 | subset |
| 5 | `from_subfinder_k2am_active` | corporate_k2am_active_oI | 8 | subset |
| 6 | `from_subfinder_upside_com` | corporate_upside_com_passive_cs | 12 | subset |
| 7 | `from_subfinder_sbs` | enterprise_sbs_passive_cs | 50 | high |
| 8 | `from_subfinder_invalid_clean_miss` | invalid_domain_clean_miss | 1 bogus | 0 |

## Harvest

```bash
python .seed/scripts/cli_corpus/prepare_httpx_hosts_from_subfinder.py
python .seed/scripts/cli_corpus/harvest.py --tool httpx
```
