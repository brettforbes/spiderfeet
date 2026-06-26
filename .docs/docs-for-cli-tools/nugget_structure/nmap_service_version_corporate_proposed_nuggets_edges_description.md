# Nmap OSINT Scan Report — service_version_corporate

## Introduction

This report narrates the findings of a **Nmap** scan against **bbc.co.uk**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **bbc.co.uk** from **Fri Jun 26 03:59:36 2026**. The operator invoked: `nmap -sT -sV -T3 -p 80,443 -oX - bbc.co.uk`.
 The run completed in **15.40** seconds.

Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds

During this scan, **1** host was placed under investigation.

## Host 151.101.128.81

The host was observed as **up** (reason: **syn-ack**).
It answers to the internet name **bbc.co.uk**.

### Networks

Network address **151.101.128.81**:
- Port **443** on **tcp** is **open** (syn-ack), associated with **https**.
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.

### Applications

Application service **http** listening on port **80**. It runs **Varnish**.
Application service **https** listening on port **443**. It runs **Varnish**.

## Conclusion

The scan captured **24** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:151.101.128.81` |
| CATEGORY | NETWORKS | Networks Category | `networks:151.101.128.81` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `syn-ack` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -sV -T3 -p 80,443 -oX - bbc.co.uk` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `15.40` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:59:36 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:59:51 2026; 1 IP address (1 host up) scanned in 15.40 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `bbc.co.uk` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `151.101.128.81` |
| ENTITY | INTERNET_NAME | Internet Name | `bbc.co.uk` |
| ENTITY | IP_ADDRESS | IP Address | `151.101.128.81` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:bbc.co.uk:Fri Jun 26 03:59:36 2026` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | SERVICE | Network Service | `https` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | PORT | Network Port | `443` |
| SUBENTITY | PORT | Network Port | `80` |
| SUBENTITY | SOFTWARE_USED | Software Used | `Varnish` |

---

*OS-Intel Scan · Fri Jun 26 03:59:36 2026 · Page 1*
