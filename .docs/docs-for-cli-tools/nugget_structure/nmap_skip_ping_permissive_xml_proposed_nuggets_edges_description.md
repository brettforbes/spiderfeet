# Nmap OSINT Scan Report — skip_ping_permissive_xml

## Introduction

This report narrates the findings of a **Nmap** scan against **scanme.nmap.org**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **scanme.nmap.org** from **Fri Jun 26 03:56:03 2026**. The operator invoked: `nmap -sT -Pn -T3 -p 80 -oX - scanme.nmap.org`.
 The run completed in **0.31** seconds.

Nmap done at Fri Jun 26 03:56:03 2026; 1 IP address (1 host up) scanned in 0.31 seconds

During this scan, **1** host was placed under investigation.

## Host 45.33.32.156

The host was observed as **up** (reason: **user-set**).
It answers to the internet name **scanme.nmap.org**.

### Networks

Network address **45.33.32.156**:
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.

### Applications

Application service **http** listening on port **80**.

## Conclusion

The scan captured **21** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:56:03 2026; 1 IP address (1 host up) scanned in 0.31 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:45.33.32.156` |
| CATEGORY | NETWORKS | Networks Category | `networks:45.33.32.156` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `user-set` |
| DESCRIPTOR | INTERNET_NAME | Internet Name | `scanme.nmap.org` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -Pn -T3 -p 80 -oX - scanme.nmap.org` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `0.31` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:56:03 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:56:03 2026; 1 IP address (1 host up) scanned in 0.31 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `scanme.nmap.org` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `45.33.32.156` |
| ENTITY | IP_ADDRESS | IP Address | `45.33.32.156` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:scanme.nmap.org:Fri Jun 26 03:56:03 2026` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | PORT | Network Port | `80` |

---

*OS-Intel Scan · Fri Jun 26 03:56:03 2026 · Page 1*
