# Nmap OSINT Scan Report — host_discovery_local_subnet

## Introduction

This report narrates the findings of a **Nmap** scan against **192.168.1.0/24**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **192.168.1.0/24** from **Fri Jun 26 04:00:07 2026**. The operator invoked: `nmap -sn -T3 -oX - 192.168.1.0/24`.
 The run completed in **11.46** seconds.

Nmap done at Fri Jun 26 04:00:18 2026; 256 IP addresses (2 hosts up) scanned in 11.46 seconds

During this scan, **2** hosts were placed under investigation.

## Host 192.168.1.11

The host was observed as **up** (reason: **localhost-response**).

### Networks

Network address **192.168.1.11**:
- No transport endpoints were enumerated.

## Host 192.168.1.9

The host was observed as **up** (reason: **localhost-response**).
It answers to the internet name **host.docker.internal**.

### Networks

Network address **192.168.1.9**:
- No transport endpoints were enumerated.

## Conclusion

The scan captured **17** semantic nuggets across **2** hosts.
 Nmap done at Fri Jun 26 04:00:18 2026; 256 IP addresses (2 hosts up) scanned in 11.46 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.11` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.9` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `localhost-response` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sn -T3 -oX - 192.168.1.0/24` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `11.46` |
| DESCRIPTOR | SCAN_START | Scan Start | `Fri Jun 26 04:00:07 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Fri Jun 26 04:00:18 2026; 256 IP addresses (2 hosts up) scanned in 11.46 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `192.168.1.0/24` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| ENTITY | HOST | Host | `192.168.1.11` |
| ENTITY | HOST | Host | `192.168.1.9` |
| ENTITY | INTERNET_NAME | Internet Name | `host.docker.internal` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.11` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.9` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:192.168.1.0/24:Fri Jun 26 04:00:07 2026` |

---

*OS-Intel Scan · Fri Jun 26 04:00:07 2026 · Page 1*
