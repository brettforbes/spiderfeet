# Nmap — Formal Examination Plan

**Tool:** Nmap 7.80 (Windows, TCP connect `-sT`)  
**Binding:** `.seed/04_Driving and Integrating_CLI_Apps.md` §2.2.3  
**Exploration report:** [nmap_exploration_report.md](nmap_exploration_report.md)  
**Manifest:** `.seed/scripts/cli_corpus/manifests/nmap.yaml`  
**Strategy:** `.strategy/nmap_strategy.skill`

## Objectives

Capture paired **XML + text** evidence for every semantic archetype (A–L) so the module can derive nugget graphs from `-oX` and present native text in the CLI Profiling UI.

## Targets

| ID | Target | Class |
|----|--------|-------|
| T1 | `scanme.nmap.org` | Permissive |
| T2 | `bbc.co.uk` | Corporate |
| T3 | `192.168.1.0/24` | Local discovery |
| T4 | `192.168.1.12` | Local Windows enrich |

## Scenario matrix

Each row = two harvest runs (`*_xml`, `*_text`).

| # | Scenario prefix | Archetype | Target | Command core | Expected semantics |
|---|-----------------|-----------|--------|--------------|-------------------|
| 1 | `host_discovery_permissive` | A | T1 | `-sn` | Host up, IPv4, hostname, IPv6 hint |
| 2 | `tcp_top_ports_permissive` | C | T1 | `-sT --top-ports 1000 --open` | Open TCP ports, service names |
| 3 | `service_version_permissive` | E | T1 | `-sT -sV -p 22,80,443,9929,31337` | Product/version on open ports |
| 4 | `os_aggressive_permissive` | F | T1 | `-sT -A -p 22,80,443` | `osmatch`, versions, NSE |
| 5 | `nse_default_permissive` | G | T1 | `-sT -sC -p 22,80,443` | Script tables (ssh-hostkey, http-title) |
| 6 | `udp_top_permissive` | H | T1 | `-sU --top-ports 20` | UDP open / closed / open\|filtered |
| 7 | `traceroute_permissive` | I | T1 | `-sT --traceroute -p 80` | Hop IPs and hostnames |
| 8 | `skip_ping_permissive` | J | T1 | `-sT -Pn -p 80` | Port scan without host discovery |
| 9 | `capstone_permissive` | K | T1 | `-sT -A --top-ports 1000 --open` | All-in-one permissive |
| 10 | `host_discovery_corporate` | A/D | T2 | `-sn` | Corporate host up |
| 11 | `tcp_top_ports_corporate` | D | T2 | `-sT --top-ports 20` | Mostly filtered; 80/443 open |
| 12 | `service_version_corporate` | E | T2 | `-sT -sV -p 80,443` | Versions on CDN web ports |
| 13 | `host_discovery_local_subnet` | B | T3 | `-sn` | Multiple LAN hosts up |
| 14 | `tcp_top_ports_local` | C | T3 | `-sT --top-ports 100 --open` | LAN open ports per host |
| 15 | `windows_enrich_local` | L | T4 | `-sT -sV -A -p 135,445,8000` | Windows RPC/SMB/http-alt + NSE |

**Total examinations:** 30 (15 archetypes × 2 output modes)

## Output rules

- XML scenarios: `-oX -` (stdout → `*_output_structured.xml`)
- Text scenarios: no `-oX` (stdout → `*_output_text.txt`)
- Timing: `-T3` unless noted in manifest
- Review status: `pending` until operator approves in CLI Profiling UI

## Execution

```bash
python .seed/scripts/cli_corpus/harvest.py --tool nmap --dry-run
python .seed/scripts/cli_corpus/harvest.py --tool nmap
```

## Post-examination

1. Draft `nugget_structure/nmap_nugget_graph_structure.md` per archetype family  
2. Propose `nodes[]` / `edges[]` JSON aligned with `.seed/05_Onotology_for_Nuggets.md`  
3. Operator review → `approved` / `rejected` on each `*_review.status.json`  
4. Advance `corpus_index.json` → `nugget_proposal`

## Verification

- [ ] 30 evidence bundles under `app_examination_docs/nmap/`
- [ ] Permissive scans show open + filtered + version + OS + NSE + UDP + traceroute
- [ ] Corporate scans show filtered-heavy matrix
- [ ] Local scans show ≥2 hosts and Windows enrichment
- [ ] CLI corpus API lists tools with `exam_count` ≥ 30
