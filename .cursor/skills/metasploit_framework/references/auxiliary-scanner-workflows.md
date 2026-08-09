# Auxiliary Scanner Workflows

Discovery-first path for SpiderFeet graph building and legal-safe defaults.

## Recommended sequence

1. `msfdb init` / `db_status` connected  
2. `workspace -a <scenario>` → `workspace <scenario>`  
3. `search type:auxiliary scanner <proto|product>`  
4. `use auxiliary/scanner/...` (or `auxiliary/gather/...`)  
5. `info` → `show options` → `show advanced`  
6. `set RHOSTS` (and `RPORT`, threads, creds)  
7. `run`  
8. `hosts` / `services` / `vulns` / `notes`  
9. Optional second module on narrowed hosts  
10. `db_export` → nugget mapping  

## Search heuristics

```text
search type:auxiliary scanner http
search type:auxiliary scanner smb
search type:auxiliary gather
search cve:2021-44228
search name:ssl version
```

Prefer modules that write hosts/services into the DB and have `documentation/modules/**` coverage.

## Pairing with external tools

| Upstream | Role |
|----------|------|
| **nmap** / **naabu** | Broad port map → `db_nmap` or feed `RHOSTS` |
| **httpx** | Confirm live HTTP before HTTP aux modules |
| **nuclei** | Template CVE pass — do not replace with random exploit modules |
| **nerva** | Service fingerprint on open ports |

## Example — SMB version (lab net)

```text
workspace lab_smb
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.56.0/24
run
hosts
services
```

## Example — TCP portscan module vs naabu

Use MSF `auxiliary/scanner/portscan/*` when you need results **inside** the MSF workspace for later modules. Prefer **naabu**/**nmap** for mass inventory destined for SpiderFeet nmap/naabu adapters.

## Empty or sparse results

1. Confirm host reachability outside MSF (ping/nmap).  
2. Verify `RHOSTS` syntax (CIDR, ranges — see shipped `msfconsole.md`).  
3. Try a different scanner family (SMB vs HTTP vs discovery).  
4. Record clean miss only when the target class is intentionally negative.  
