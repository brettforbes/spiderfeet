# Nmap OSINT Scan Report — udp_top_permissive_xml

## Introduction

This report narrates the findings of a **Nmap** scan against **scanme.nmap.org**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **scanme.nmap.org** from **Fri Jun 26 03:55:32 2026**. The operator invoked: `nmap -sU -T3 --top-ports 20 -oX - scanme.nmap.org`.
 The run completed in **15.60** seconds.

Nmap done at Fri Jun 26 03:55:47 2026; 1 IP address (1 host up) scanned in 15.60 seconds

During this scan, **1** host was placed under investigation.

## Host 45.33.32.156

The host was observed as **up** (reason: **reset**).
It answers to the internet name **scanme.nmap.org**.

### Networks

Network address **45.33.32.156**:
- Port **123** on **udp** is **open** (udp-response), associated with **ntp**.
- Port **135** on **udp** is **open|filtered** (no-response), associated with **msrpc**.
- Port **137** on **udp** is **open|filtered** (no-response), associated with **netbios-ns**.
- Port **138** on **udp** is **open|filtered** (no-response), associated with **netbios-dgm**.
- Port **139** on **udp** is **open|filtered** (no-response), associated with **netbios-ssn**.
- Port **1434** on **udp** is **closed** (port-unreach), associated with **ms-sql-m**.
- Port **161** on **udp** is **closed** (port-unreach), associated with **snmp**.
- Port **162** on **udp** is **closed** (port-unreach), associated with **snmptrap**.
- Port **1900** on **udp** is **closed** (port-unreach), associated with **upnp**.
- Port **445** on **udp** is **closed** (port-unreach), associated with **microsoft-ds**.
- Port **4500** on **udp** is **closed** (port-unreach), associated with **nat-t-ike**.
- Port **49152** on **udp** is **closed** (port-unreach), associated with **unknown**.
- Port **500** on **udp** is **closed** (port-unreach), associated with **isakmp**.
- Port **514** on **udp** is **closed** (port-unreach), associated with **syslog**.
- Port **520** on **udp** is **closed** (port-unreach), associated with **route**.
- Port **53** on **udp** is **closed** (port-unreach), associated with **domain**.
- Port **631** on **udp** is **closed** (port-unreach), associated with **ipp**.
- Port **67** on **udp** is **open|filtered** (no-response), associated with **dhcps**.
- Port **68** on **udp** is **open|filtered** (no-response), associated with **dhcpc**.
- Port **69** on **udp** is **closed** (port-unreach), associated with **tftp**.

### Applications

Application service **dhcpc** listening on port **68**.
Application service **dhcps** listening on port **67**.
Application service **domain** listening on port **53**.
Application service **ipp** listening on port **631**.
Application service **isakmp** listening on port **500**.
Application service **microsoft-ds** listening on port **445**.
Application service **ms-sql-m** listening on port **1434**.
Application service **msrpc** listening on port **135**.
Application service **nat-t-ike** listening on port **4500**.
Application service **netbios-dgm** listening on port **138**.
Application service **netbios-ns** listening on port **137**.
Application service **netbios-ssn** listening on port **139**.
Application service **ntp** listening on port **123**.
Application service **route** listening on port **520**.
Application service **snmp** listening on port **161**.
Application service **snmptrap** listening on port **162**.
Application service **syslog** listening on port **514**.
Application service **tftp** listening on port **69**.
Application service **unknown** listening on port **49152**.
Application service **upnp** listening on port **1900**.

## Conclusion

The scan captured **63** semantic nuggets across **1** host.
 Nmap done at Fri Jun 26 03:55:47 2026; 1 IP address (1 host up) scanned in 15.60 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:45.33.32.156` |
| CATEGORY | NETWORKS | Networks Category | `networks:45.33.32.156` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `reset` |
| DESCRIPTOR | INTERNET_NAME | Internet Name | `scanme.nmap.org` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `udp` |
| DESCRIPTOR | PORT_STATE | Port State | `closed` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE | Port State | `open\|filtered` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `no-response` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `port-unreach` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `udp-response` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sU -T3 --top-ports 20 -oX - scanme.nmap.org` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `15.60` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 03:55:32 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 03:55:47 2026; 1 IP address (1 host up) scanned in 15.60 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `scanme.nmap.org` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `45.33.32.156` |
| ENTITY | IPV4_ADDRESS | IP Address | `45.33.32.156` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:scanme.nmap.org:Fri Jun 26 03:55:32 2026` |
| ENTITY | SERVICE | Network Service | `dhcpc` |
| ENTITY | SERVICE | Network Service | `dhcps` |
| ENTITY | SERVICE | Network Service | `domain` |
| ENTITY | SERVICE | Network Service | `ipp` |
| ENTITY | SERVICE | Network Service | `isakmp` |
| ENTITY | SERVICE | Network Service | `microsoft-ds` |
| ENTITY | SERVICE | Network Service | `ms-sql-m` |
| ENTITY | SERVICE | Network Service | `msrpc` |
| ENTITY | SERVICE | Network Service | `nat-t-ike` |
| ENTITY | SERVICE | Network Service | `netbios-dgm` |
| ENTITY | SERVICE | Network Service | `netbios-ns` |
| ENTITY | SERVICE | Network Service | `netbios-ssn` |
| ENTITY | SERVICE | Network Service | `ntp` |
| ENTITY | SERVICE | Network Service | `route` |
| ENTITY | SERVICE | Network Service | `snmp` |
| ENTITY | SERVICE | Network Service | `snmptrap` |
| ENTITY | SERVICE | Network Service | `syslog` |
| ENTITY | SERVICE | Network Service | `tftp` |
| ENTITY | SERVICE | Network Service | `unknown` |
| ENTITY | SERVICE | Network Service | `upnp` |
| ENTITY | TRANSPORT | Transport Protocol | `udp` |
| SUBENTITY | PORT | Network Port | `123` |
| SUBENTITY | PORT | Network Port | `135` |
| SUBENTITY | PORT | Network Port | `137` |
| SUBENTITY | PORT | Network Port | `138` |
| SUBENTITY | PORT | Network Port | `139` |
| SUBENTITY | PORT | Network Port | `1434` |
| SUBENTITY | PORT | Network Port | `161` |
| SUBENTITY | PORT | Network Port | `162` |
| SUBENTITY | PORT | Network Port | `1900` |
| SUBENTITY | PORT | Network Port | `445` |
| SUBENTITY | PORT | Network Port | `4500` |
| SUBENTITY | PORT | Network Port | `49152` |
| SUBENTITY | PORT | Network Port | `500` |
| SUBENTITY | PORT | Network Port | `514` |
| SUBENTITY | PORT | Network Port | `520` |
| SUBENTITY | PORT | Network Port | `53` |
| SUBENTITY | PORT | Network Port | `631` |
| SUBENTITY | PORT | Network Port | `67` |
| SUBENTITY | PORT | Network Port | `68` |
| SUBENTITY | PORT | Network Port | `69` |

---

*OS-Intel Scan · Fri Jun 26 03:55:32 2026 · Page 1*
