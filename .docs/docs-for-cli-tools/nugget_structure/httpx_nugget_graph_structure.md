# httpx nugget graph structure

## Pipeline

**Input:** Host lists extracted from subfinder formal examinations (`prepare_httpx_hosts_from_subfinder.py`).  
**Probe:** `httpx -l hosts.txt -status-code -title -tech-detect -server -cdn -ip -json`.

## Scan head

- `SCAN_RECORD` — apex target domain
- `SCAN_CLI` — full httpx command
- `DOMAIN_NAME` — seed apex

## Per live URL record

| httpx field | Nugget | Edge |
|-------------|--------|------|
| `url` | `LINKED_URL_INTERNAL` | scan `contains` |
| `host` | `INTERNET_NAME` | domain `contains`; URL `contains` |
| `ip` | `IP_ADDRESS` | host `contains` |
| `status_code` | `HTTP_CODE` | URL `had` |
| `webserver` | `WEBSERVER_BANNER` | URL `had` |
| `tech[]` | `WEBSERVER_TECHNOLOGY` | URL `had` each |
| `cdn_name` / `cdn` | `PROVIDER_HOSTING` | URL `had` |

## Subfinder linkage

Each httpx scenario documents `subfinder_scenario` in bundle metadata and `host_input_count` vs `probe_summary_lines` (live web hits).

## Scenarios

| httpx scenario | Subfinder source | Role |
|----------------|------------------|------|
| `from_subfinder_upside_au` | `corporate_upside_au_passive_cs` | Rich SME web surface |
| `from_subfinder_squarepeg` | `corporate_squarepeg_passive_cs` | Small VC |
| `from_subfinder_vcof_sparse` | `corporate_vcof_sparse_passive` | Ultra-sparse |
| `from_subfinder_k2am_passive` | `corporate_k2am_passive_cs` | Hosting-style SME |
| `from_subfinder_k2am_active` | `corporate_k2am_active_oI` | Resolved subset |
| `from_subfinder_upside_com` | `corporate_upside_com_passive_cs` | TLD sibling |
| `from_subfinder_sbs` | `enterprise_sbs_passive_cs` | Enterprise volume |
| `from_subfinder_invalid_clean_miss` | `invalid_domain_clean_miss` | Clean miss |
