# Nmap OSINT Scan Report — tcp_top_ports_corporate

## Introduction

This report narrates the findings of a **Nmap** scan against **bbc.co.uk**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **bbc.co.uk** from **Fri Jun 26 03:59:31 2026**. The operator invoked: `nmap -sT -T3 --top-ports 20 -oX - bbc.co.uk`.
 The run completed in **2.33** seconds.

Nmap done at Fri Jun 26 03:59:33 2026; 1 IP address (1 host up) scanned in 2.33 seconds

During this scan, **1** host was placed under investigation.

## Host 151.101.128.81

The host was observed as **up** (reason: **syn-ack**).
It answers to the internet name **bbc.co.uk**.

### Networks

Network address **151.101.128.81**:
- Port **110** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **111** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **135** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **139** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **143** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **1723** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **21** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **22** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **23** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **25** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **3306** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **3389** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **443** on **tcp** is **open** (syn-ack), associated with **https**.
- Port **445** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **53** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **5900** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.
- Port **8080** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **993** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.
- Port **995** on **tcp** is **filtered** (no-response), associated with **an unnamed service**.

### Applications

Application service **domain**.
Application service **ftp**.
Application service **http** listening on port **80**.
Application service **http-proxy**.
Application service **https** listening on port **443**.
Application service **imap**.
Application service **imaps**.
Application service **microsoft-ds**.
Application service **ms-wbt-server**.
Application service **msrpc**.
Application service **mysql**.
Application service **netbios-ssn**.
Application service **pop3**.
Application service **pop3s**.
Application service **pptp**.
Application service **rpcbind**.
Application service **smtp**.
Application service **ssh**.
Application service **telnet**.
Application service **vnc**.

## Conclusion

The scan captured **61** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:59:33 2026; 1 IP address (1 host up) scanned in 2.33 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:151.101.128.81` |
| CATEGORY | NETWORKS | Networks Category | `networks:151.101.128.81` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `syn-ack` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `filtered` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `no-response` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -T3 --top-ports 20 -oX - bbc.co.uk` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `2.33` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:59:31 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:59:33 2026; 1 IP address (1 host up) scanned in 2.33 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `bbc.co.uk` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `151.101.128.81` |
| ENTITY | INTERNET_NAME | Internet Name | `bbc.co.uk` |
| ENTITY | IP_ADDRESS | IP Address | `151.101.128.81` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:bbc.co.uk:Fri Jun 26 03:59:31 2026` |
| ENTITY | SERVICE | Network Service | `domain` |
| ENTITY | SERVICE | Network Service | `ftp` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | SERVICE | Network Service | `http-proxy` |
| ENTITY | SERVICE | Network Service | `https` |
| ENTITY | SERVICE | Network Service | `imap` |
| ENTITY | SERVICE | Network Service | `imaps` |
| ENTITY | SERVICE | Network Service | `microsoft-ds` |
| ENTITY | SERVICE | Network Service | `ms-wbt-server` |
| ENTITY | SERVICE | Network Service | `msrpc` |
| ENTITY | SERVICE | Network Service | `mysql` |
| ENTITY | SERVICE | Network Service | `netbios-ssn` |
| ENTITY | SERVICE | Network Service | `pop3` |
| ENTITY | SERVICE | Network Service | `pop3s` |
| ENTITY | SERVICE | Network Service | `pptp` |
| ENTITY | SERVICE | Network Service | `rpcbind` |
| ENTITY | SERVICE | Network Service | `smtp` |
| ENTITY | SERVICE | Network Service | `ssh` |
| ENTITY | SERVICE | Network Service | `telnet` |
| ENTITY | SERVICE | Network Service | `vnc` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | PORT | Network Port | `110` |
| SUBENTITY | PORT | Network Port | `111` |
| SUBENTITY | PORT | Network Port | `135` |
| SUBENTITY | PORT | Network Port | `139` |
| SUBENTITY | PORT | Network Port | `143` |
| SUBENTITY | PORT | Network Port | `1723` |
| SUBENTITY | PORT | Network Port | `21` |
| SUBENTITY | PORT | Network Port | `22` |
| SUBENTITY | PORT | Network Port | `23` |
| SUBENTITY | PORT | Network Port | `25` |
| SUBENTITY | PORT | Network Port | `3306` |
| SUBENTITY | PORT | Network Port | `3389` |
| SUBENTITY | PORT | Network Port | `443` |
| SUBENTITY | PORT | Network Port | `445` |
| SUBENTITY | PORT | Network Port | `53` |
| SUBENTITY | PORT | Network Port | `5900` |
| SUBENTITY | PORT | Network Port | `80` |
| SUBENTITY | PORT | Network Port | `8080` |
| SUBENTITY | PORT | Network Port | `993` |
| SUBENTITY | PORT | Network Port | `995` |

---

*OS-Intel Scan · Fri Jun 26 03:59:31 2026 · Page 1*
