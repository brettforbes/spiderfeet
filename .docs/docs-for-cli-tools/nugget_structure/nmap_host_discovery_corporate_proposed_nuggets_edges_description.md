# Nmap OSINT Scan Report — host_discovery_corporate

## Introduction

This report narrates the findings of a **Nmap** scan against **bbc.co.uk**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **bbc.co.uk** from **Fri Jun 26 03:59:30 2026**. The operator invoked: `nmap -sn -T3 -oX - bbc.co.uk`.
 The run completed in **0.34** seconds.

Nmap done at Fri Jun 26 03:59:30 2026; 1 IP address (1 host up) scanned in 0.34 seconds

During this scan, **1** host was placed under investigation.

## Host 151.101.128.81

The host was observed as **up** (reason: **syn-ack**).
It answers to the internet name **bbc.co.uk**.

### Networks

Network address **151.101.128.81**:
- No transport endpoints were enumerated.

## Conclusion

The scan captured **14** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:59:30 2026; 1 IP address (1 host up) scanned in 0.34 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | NETWORKS | Networks Category | `networks:151.101.128.81` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sn -T3 -oX - bbc.co.uk` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `0.34` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:59:30 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:59:30 2026; 1 IP address (1 host up) scanned in 0.34 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `bbc.co.uk` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `151.101.128.81` |
| ENTITY | INTERNET_NAME | Internet Name | `bbc.co.uk` |
| ENTITY | IP_ADDRESS | IP Address | `151.101.128.81` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:bbc.co.uk:Fri Jun 26 03:59:30 2026` |

---

*OS-Intel Scan · Fri Jun 26 03:59:30 2026 · Page 1*
