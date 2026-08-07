# Nmap OSINT Scan Report — tcp_top_ports_local_xml

## Introduction

This report narrates the findings of a **Nmap** scan against **192.168.1.0/24**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **192.168.1.0/24** from **Fri Jun 26 04:00:30 2026**. The operator invoked: `nmap -sT -T3 --top-ports 100 --open -oX - 192.168.1.0/24`.
 The run completed in **21.75** seconds.

Nmap done at Fri Jun 26 04:00:52 2026; 256 IP addresses (2 hosts up) scanned in 21.75 seconds

During this scan, **2** hosts were placed under investigation.

## Host 192.168.1.11

The host was observed as **up** (reason: **localhost-response**).

### Networks

Network address **192.168.1.11**:
- Port **135** on **tcp** is **open** (syn-ack), associated with **msrpc**.
- Port **139** on **tcp** is **open** (syn-ack), associated with **netbios-ssn**.
- Port **3000** on **tcp** is **open** (syn-ack), associated with **ppp**.
- Port **445** on **tcp** is **open** (syn-ack), associated with **microsoft-ds**.
- Port **8000** on **tcp** is **open** (syn-ack), associated with **http-alt**.

### Applications

Application service **http-alt** listening on port **8000**.
Application service **microsoft-ds** listening on port **445**.
Application service **msrpc** listening on port **135**.
Application service **netbios-ssn** listening on port **139**.
Application service **ppp** listening on port **3000**.

## Host 192.168.1.9

The host was observed as **up** (reason: **localhost-response**).
It answers to the internet name **host.docker.internal**.

### Networks

Network address **192.168.1.9**:
- Port **135** on **tcp** is **open** (syn-ack), associated with **msrpc**.
- Port **139** on **tcp** is **open** (syn-ack), associated with **netbios-ssn**.
- Port **3000** on **tcp** is **open** (syn-ack), associated with **ppp**.
- Port **445** on **tcp** is **open** (syn-ack), associated with **microsoft-ds**.
- Port **8000** on **tcp** is **open** (syn-ack), associated with **http-alt**.

### Applications

Application service **http-alt** listening on port **8000**.
Application service **microsoft-ds** listening on port **445**.
Application service **msrpc** listening on port **135**.
Application service **netbios-ssn** listening on port **139**.
Application service **ppp** listening on port **3000**.

## Conclusion

The scan captured **33** semantic nuggets across **2** hosts.
 Nmap done at Fri Jun 26 04:00:52 2026; 256 IP addresses (2 hosts up) scanned in 21.75 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:192.168.1.11` |
| CATEGORY | APPLICATIONS | Applications Category | `applications:192.168.1.9` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.11` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.9` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `localhost-response` |
| DESCRIPTOR | INTERNET_NAME | Internet Name | `host.docker.internal` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -T3 --top-ports 100 --open -oX - 192.168.1.0/24` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `21.75` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 04:00:30 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 04:00:52 2026; 256 IP addresses (2 hosts up) scanned in 21.75 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `192.168.1.0/24` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `192.168.1.11` |
| ENTITY | HOST | Host | `192.168.1.9` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.11` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.9` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:192.168.1.0/24:Fri Jun 26 04:00:30 2026` |
| ENTITY | SERVICE | Network Service | `http-alt` |
| ENTITY | SERVICE | Network Service | `microsoft-ds` |
| ENTITY | SERVICE | Network Service | `msrpc` |
| ENTITY | SERVICE | Network Service | `netbios-ssn` |
| ENTITY | SERVICE | Network Service | `ppp` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | PORT | Network Port | `135` |
| SUBENTITY | PORT | Network Port | `139` |
| SUBENTITY | PORT | Network Port | `3000` |
| SUBENTITY | PORT | Network Port | `445` |
| SUBENTITY | PORT | Network Port | `8000` |

---

*OS-Intel Scan · Fri Jun 26 04:00:30 2026 · Page 1*
