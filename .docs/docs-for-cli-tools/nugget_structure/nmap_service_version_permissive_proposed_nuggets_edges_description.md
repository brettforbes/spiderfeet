# Nmap OSINT Scan Report — service_version_permissive_xml

## Introduction

This report narrates the findings of a **Nmap** scan against **scanme.nmap.org**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **scanme.nmap.org** from **Tue Jun 23 19:00:44 2026**. The operator invoked: `nmap -sT -sV -T3 -p 22,80,443,9929,31337 -oX - scanme.nmap.org`.
 The run completed in **11.20** seconds.

Nmap done at Tue Jun 23 19:00:55 2026; 1 IP address (1 host up) scanned in 11.20 seconds

During this scan, **1** host was placed under investigation.

## Host 45.33.32.156

The host was observed as **up** (reason: **echo-reply**).
It answers to the internet name **scanme.nmap.org**.

### Networks

Network address **45.33.32.156**:
- Port **22** on **tcp** is **open** (syn-ack), associated with **ssh**.
- Port **31337** on **tcp** is **open** (syn-ack), associated with **tcpwrapped**.
- Port **443** on **tcp** is **filtered** (no-response), associated with **https**.
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.
- Port **9929** on **tcp** is **filtered** (no-response), associated with **nping-echo**.

### Applications

Application service **http** listening on port **80**. It runs **Apache httpd 2.4.7**. Additional detail: **(Ubuntu)**.
- Common Platform Enumeration: `cpe:/a:apache:http_server:2.4.7`.
Application service **https** listening on port **443**.
Application service **nping-echo** listening on port **9929**.
Application service **ssh** listening on port **22**. It runs **OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13**. Additional detail: **Ubuntu Linux; protocol 2.0**.
- Common Platform Enumeration: `cpe:/a:openbsd:openssh:6.6.1p1`.
- Common Platform Enumeration: `cpe:/o:linux:linux_kernel`.
Application service **tcpwrapped** listening on port **31337**.

## Conclusion

The scan captured **38** semantic nuggets across **1** host.
 Nmap done at Tue Jun 23 19:00:55 2026; 1 IP address (1 host up) scanned in 11.20 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:45.33.32.156` |
| CATEGORY | NETWORKS | Networks Category | `networks:45.33.32.156` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `echo-reply` |
| DESCRIPTOR | INTERNET_NAME | Internet Name | `scanme.nmap.org` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `filtered` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `no-response` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -sV -T3 -p 22,80,443,9929,31337 -oX - scanme.nmap.org` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `11.20` |
| DESCRIPTOR | SCAN_START | Scan Start | `Tue Jun 23 19:00:44 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Tue Jun 23 19:00:55 2026; 1 IP address (1 host up) scanned in 11.20 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `scanme.nmap.org` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| DESCRIPTOR | SERVICE_EXTRAINFO | Service Extra Information | `(Ubuntu)` |
| DESCRIPTOR | SERVICE_EXTRAINFO | Service Extra Information | `Ubuntu Linux; protocol 2.0` |
| DESCRIPTOR | SERVICE_VERSION | Service Version | `Apache httpd 2.4.7` |
| DESCRIPTOR | SERVICE_VERSION | Service Version | `OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13` |
| ENTITY | HOST | Host | `45.33.32.156` |
| ENTITY | IP_ADDRESS | IP Address | `45.33.32.156` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:scanme.nmap.org:Tue Jun 23 19:00:44 2026` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | SERVICE | Network Service | `https` |
| ENTITY | SERVICE | Network Service | `nping-echo` |
| ENTITY | SERVICE | Network Service | `ssh` |
| ENTITY | SERVICE | Network Service | `tcpwrapped` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | CPE_URL | CPE URL | `cpe:/a:apache:http_server:2.4.7` |
| SUBENTITY | CPE_URL | CPE URL | `cpe:/a:openbsd:openssh:6.6.1p1` |
| SUBENTITY | CPE_URL | CPE URL | `cpe:/o:linux:linux_kernel` |
| SUBENTITY | PORT | Network Port | `22` |
| SUBENTITY | PORT | Network Port | `31337` |
| SUBENTITY | PORT | Network Port | `443` |
| SUBENTITY | PORT | Network Port | `80` |
| SUBENTITY | PORT | Network Port | `9929` |

---

*OS-Intel Scan · Tue Jun 23 19:00:44 2026 · Page 1*
