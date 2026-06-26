# Nmap OSINT Scan Report — windows_enrich_local

## Introduction

This report narrates the findings of a **Nmap** scan against **192.168.1.12**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **192.168.1.12** from **Fri Jun 26 04:01:18 2026**. The operator invoked: `nmap -sT -sV -A -T3 -p 135,445,8000 -oX - 192.168.1.12`.
 The run completed in **2.49** seconds.

Nmap done at Fri Jun 26 04:01:20 2026; 1 IP address (0 hosts up) scanned in 2.49 seconds

During this scan, **0** hosts were placed under investigation.

## Conclusion

The scan captured **8** semantic nuggets across **0** hosts.
 Nmap done at Fri Jun 26 04:01:20 2026; 1 IP address (0 hosts up) scanned in 2.49 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -sV -A -T3 -p 135,445,8000 -oX - 192.168.1.12` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `2.49` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 04:01:18 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 04:01:20 2026; 1 IP address (0 hosts up) scanned in 2.49 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `192.168.1.12` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:192.168.1.12:Fri Jun 26 04:01:18 2026` |

---

*OS-Intel Scan · Fri Jun 26 04:01:18 2026 · Page 1*
