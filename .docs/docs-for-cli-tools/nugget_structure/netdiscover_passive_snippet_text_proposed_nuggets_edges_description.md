# Netdiscover OSINT Scan Report — passive_snippet_text

## Introduction

This report narrates the findings of a **Netdiscover** ARP discovery run for **netdiscover — C — passive ARP snippet (bounded)**. The story follows the scan metadata, each discovered **system** on the segment, and the **networks** inventory (IPv4, MAC, and vendor) attached to every system. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan started at **Mon Jun 29 14:34:57 2026** with arguments `netdiscover — C — passive ARP snippet (bounded)`.
 It finished at **Mon Jun 29 14:35:14 2026**.
 Exit status: **success**.

NetDiscover done at Mon Jun 29 14:35:14 2026; 12 Systems Discovered, 4 Scan Tries, 3 Empty Scans, scanned in 16.88 seconds

Netdiscover recorded **4** scan frame(s), **3** empty scan(s) before settling on the host table used for this graph.
**12** system(s) appear in the structured host inventory.
**12** system node(s) are linked from the scan record in this graph.

### Scan topology

```mermaid
flowchart TD
  scan["SCAN_RECORD"]
  sys1["SYSTEM 192.168.1.1"]
  scan -->|contains| sys1
  sys2["SYSTEM 192.168.1.10"]
  scan -->|contains| sys2
  sys3["SYSTEM 192.168.1.14"]
  scan -->|contains| sys3
  sys4["SYSTEM 192.168.1.15"]
  scan -->|contains| sys4
  sys5["SYSTEM 192.168.1.16"]
  scan -->|contains| sys5
  sys6["SYSTEM 192.168.1.2"]
  scan -->|contains| sys6
  sys7["SYSTEM 192.168.1.250"]
  scan -->|contains| sys7
  sys8["SYSTEM 192.168.1.3"]
  scan -->|contains| sys8
  sys9["SYSTEM 192.168.1.4"]
  scan -->|contains| sys9
  sys10["SYSTEM 192.168.1.6"]
  scan -->|contains| sys10
  sys11["SYSTEM 192.168.1.7"]
  scan -->|contains| sys11
  sys12["SYSTEM 192.168.1.8"]
  scan -->|contains| sys12
```

## System 192.168.1.1

System **192.168.1.1** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.1"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.1**.
- MAC address **14:5f:94:d8:7a:5f** — vendor **Unknown**.

## System 192.168.1.10

System **192.168.1.10** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.10"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.10**.
- MAC address **26:87:b6:2f:b0:73** — vendor **Unknown**.

## System 192.168.1.14

System **192.168.1.14** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.14"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.14**.
- MAC address **02:0f:b5:b7:bd:29** — vendor **Unknown**.

## System 192.168.1.15

System **192.168.1.15** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.15"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.15**.
- MAC address **5a:ba:45:91:e3:41** — vendor **Unknown**.

## System 192.168.1.16

System **192.168.1.16** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.16"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.16**.
- MAC address **3e:48:b2:24:45:34** — vendor **Unknown**.

## System 192.168.1.2

System **192.168.1.2** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.2"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.2**.
- MAC address **02:0f:b5:23:c6:49** — vendor **Unknown**.

## System 192.168.1.250

System **192.168.1.250** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.250"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.250**.
- MAC address **02:0f:b5:46:32:8f** — vendor **Unknown**.

## System 192.168.1.3

System **192.168.1.3** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.3"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.3**.
- MAC address **3c:a3:08:a4:d1:8d** — vendor **Unknown**.

## System 192.168.1.4

System **192.168.1.4** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.4"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.4**.
- MAC address **02:0f:b5:0a:e3:6c** — vendor **Unknown**.

## System 192.168.1.6

System **192.168.1.6** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.6"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.6**.
- MAC address **88:d8:2e:c2:2c:0c** — vendor **Unknown**.

## System 192.168.1.7

System **192.168.1.7** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.7"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.7**.
- MAC address **16:0c:6b:46:32:90** — vendor **Unknown**.

## System 192.168.1.8

System **192.168.1.8** was observed on the local segment during ARP discovery.

### Networks

```mermaid
flowchart TD
  system["SYSTEM 192.168.1.8"]
  nets["NETWORKS"]
  system -->|contains| nets
  ip["IP_ADDRESS"]
  nets -->|contains| ip
  mac["MAC_ADDRESS"]
  nets -->|contains| mac
  vendor["MAC_VENDOR"]
  mac -->|had| vendor
```

- IPv4 address **192.168.1.8**.
- MAC address **16:0c:6b:46:32:90** — vendor **Unknown**.

## Conclusion

The scan captured **57** semantic nuggets across **12** systems.
 NetDiscover done at Mon Jun 29 14:35:14 2026; 12 Systems Discovered, 4 Scan Tries, 3 Empty Scans, scanned in 16.88 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.1` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.10` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.14` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.15` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.16` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.2` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.250` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.3` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.4` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.6` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.7` |
| CATEGORY | NETWORKS | Networks Category | `networks:192.168.1.8` |
| DESCRIPTOR | MAC_VENDOR | MAC Vendor | `Unknown` |
| DESCRIPTOR | SCAN_ARGS | Scan Args | `netdiscover — C — passive ARP snippet (bounded)` |
| DESCRIPTOR | SCAN_DISCOVERED | Systems Discovered | `12` |
| DESCRIPTOR | SCAN_EMPTY_SCANS | Empty Scans | `3` |
| DESCRIPTOR | SCAN_END_TIME | Scan End Time | `Mon Jun 29 14:35:14 2026` |
| DESCRIPTOR | SCAN_EXIT_STATUS | Scan Exit Status | `success` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `NetDiscover done at Mon Jun 29 14:35:14 2026; 12 Systems Discovered, 4 Scan Tries, 3 Empty Scans, scanned in 16.88 seconds` |
| DESCRIPTOR | SCAN_TIMESTAMP | Scan Start Time | `Mon Jun 29 14:34:57 2026` |
| DESCRIPTOR | SCAN_TRIES | Scan Tries | `4` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.1` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.10` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.14` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.15` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.16` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.2` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.250` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.3` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.4` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.6` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.7` |
| ENTITY | IP_ADDRESS | IP Address | `192.168.1.8` |
| ENTITY | MAC_ADDRESS | MAC Address | `02:0f:b5:0a:e3:6c` |
| ENTITY | MAC_ADDRESS | MAC Address | `02:0f:b5:23:c6:49` |
| ENTITY | MAC_ADDRESS | MAC Address | `02:0f:b5:46:32:8f` |
| ENTITY | MAC_ADDRESS | MAC Address | `02:0f:b5:b7:bd:29` |
| ENTITY | MAC_ADDRESS | MAC Address | `14:5f:94:d8:7a:5f` |
| ENTITY | MAC_ADDRESS | MAC Address | `16:0c:6b:46:32:90` |
| ENTITY | MAC_ADDRESS | MAC Address | `26:87:b6:2f:b0:73` |
| ENTITY | MAC_ADDRESS | MAC Address | `3c:a3:08:a4:d1:8d` |
| ENTITY | MAC_ADDRESS | MAC Address | `3e:48:b2:24:45:34` |
| ENTITY | MAC_ADDRESS | MAC Address | `5a:ba:45:91:e3:41` |
| ENTITY | MAC_ADDRESS | MAC Address | `88:d8:2e:c2:2c:0c` |
| ENTITY | SCAN_RECORD | Scan Record | `netdiscover — C — passive ARP snippet (bounded)` |
| ENTITY | SYSTEM | System | `192.168.1.1` |
| ENTITY | SYSTEM | System | `192.168.1.10` |
| ENTITY | SYSTEM | System | `192.168.1.14` |
| ENTITY | SYSTEM | System | `192.168.1.15` |
| ENTITY | SYSTEM | System | `192.168.1.16` |
| ENTITY | SYSTEM | System | `192.168.1.2` |
| ENTITY | SYSTEM | System | `192.168.1.250` |
| ENTITY | SYSTEM | System | `192.168.1.3` |
| ENTITY | SYSTEM | System | `192.168.1.4` |
| ENTITY | SYSTEM | System | `192.168.1.6` |
| ENTITY | SYSTEM | System | `192.168.1.7` |
| ENTITY | SYSTEM | System | `192.168.1.8` |

---

*OS-Intel Scan · Mon Jun 29 14:34:57 2026 · Page 1*
