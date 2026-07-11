# Subfinder nugget graph structure

## Scan head

- `SCAN_RECORD` — apex domain target
- `SCAN_CLI` — full command (`had` from scan)
- `DOMAIN_NAME` — seed apex (`contains` from scan)

## Per-host records

| Mode | Nugget | Edge |
|------|--------|------|
| Passive | `INTERNET_NAME_UNRESOLVED` | scan `contains` host; domain `contains` host |
| Active + IP | `INTERNET_NAME` | same + `IP_ADDRESS` `contains` from host |
| Sources | `RAW_DNS_RECORDS` descriptor | `had` from host (comma-joined sources) |

## Field mapping

| JSON field | Graph |
|------------|-------|
| `host` | `INTERNET_NAME` or `INTERNET_NAME_UNRESOLVED` |
| `input` | `DOMAIN_NAME` apex |
| `sources[]` | `RAW_DNS_RECORDS` descriptor |
| `ip` | `IP_ADDRESS` under host |
| `mode` | passive vs active (bundle metadata) |

## Scenario coverage

| Scenario | Records (exploration) | Role |
|----------|----------------------|------|
| `corporate_upside_au_passive_cs` | 52 | Rich SME |
| `corporate_squarepeg_passive_cs` | 7 | Small VC |
| `corporate_vcof_sparse_passive` | 1 | Ultra-sparse |
| `corporate_k2am_passive_cs` | 18 | Hosting-style SME |
| `corporate_k2am_active_oI` | 8 | Active + IP shape |
| `corporate_upside_com_passive_cs` | 12 | TLD sibling |
| `enterprise_sbs_passive_cs` | 50 | Enterprise volume |
| `invalid_domain_clean_miss` | 0 | Clean miss |

## Intentionally unmapped

- Duplicate apex host equal to seed (skipped)
- Per-source separate nodes (collapsed to one descriptor per host)
