# Metasploit Strategies and Tactics

## Module search

- Start narrow: `type:auxiliary` + protocol/product keywords.  
- Add `platform:` / CVE when exploit research is authorized.  
- Prefer modules with `documentation/modules/**` and clear DB side effects.  
- If `search` returns exploit-heavy noise, prefix `type:auxiliary`.

## When MSF vs dedicated scanners

| Signal | Move |
|--------|------|
| Need fast open-port inventory | **naabu** / **nmap**, then optionally `db_nmap` |
| Need HTTP tech/status at scale | **httpx** |
| Need CVE templates | **nuclei** |
| Need MSF-specific protocol module + workspace | Stay in MSF aux |
| Need payload/handler lab proof | `msfvenom` + `multi/handler` |

## After `check` failure

1. Read module references — “Safe”/“Detected” meanings vary.  
2. Confirm `RHOSTS`/`RPORT`/SSL options.  
3. Try a related auxiliary scanner before any exploit.  
4. Do not escalate to `exploit` to “see if it works.”

## Empty `hosts` workspace

1. Verify L3/L4 reachability outside MSF.  
2. Fix `RHOSTS` syntax (CIDR must be full address form per shipped docs).  
3. Switch module family (discovery vs service-specific).  
4. Confirm `db_status` — without DB, hosts may not persist.  
5. Only then record clean miss for a negative fixture.

## `db_nmap` import vs native nmap profiling

- Use **`db_nmap`** when the goal is MSF workspace correlation and later aux modules.  
- Use **standalone nmap `-oX`** when the goal is SpiderFeet nmap corpus adapters — do not substitute MSF console paste for nmap XML.

## Windows package blockers (this repo)

- **GemNotFound** after admin extract → runtime blocked; document as dependency error scenario.  
- **MSI 1603** on full install → install blocked; prefer Kali/WSL or repaired Windows install for live exercise.  
- Flag documentation still valid via reconstructed OptionParser captures.

## Maximize actionable scan data

1. Workspace per scenario.  
2. Broad aux discovery → focused service modules on live hosts.  
3. Export DB after each meaningful batch.  
4. Correlate with nmap/httpx/nuclei outputs in the graph narrative — do not collapse distinct tools into one messy console log.
