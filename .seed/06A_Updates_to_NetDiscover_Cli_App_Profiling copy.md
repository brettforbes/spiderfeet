# Updates to NetDiscover CLI App Profiling

## 1. Purpose

The NetDiscover Examinations produced some outputs, but substantial work remains:

### Issue 1: Truncated output

Some results are clearly incorrectly truncated, particularly for `netdiscover — D — full /24 active rescan (parseable)` and `netdiscover — B — fast mode gateway probe 192.168.1.0/24 (parseable)`. You must make sure this never, ever happens again. **Truncation of output must be prevented at all costs.** Please update your rules to ensure this never happens again.

### Issue 2: Missing Capture of Scan CLI Command and Date Timestamp

You must make sure the CLI command and date timestamp are captured for every scan. This is critical for reproducibility and auditability. Please update your rules to ensure this is captured for every scan.


### Issue 3: Missing Capture of Scan Tries

When multiple scans are made, but return nothing. The information that must be collected is the number of times an attempt was made, as properties `scan_tries` on the scan object. Thus, the following output should be converted so that the structured form of the scan object includes the number of scan tries.

```
[H[2J[3J[1;1H[J Currently scanning: Starting.   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: (passive)   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: (passive)   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: (passive)   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: (passive)   |   Screen View: Unique Hosts         
```

### Issue 4: Missing Capture of Results Tables

CLI Apps very commonly include tables in their output. These tables must be captured and included in the structured form of the scan object. In this scan one can see multiple scan tries, some of which result in a table of results. Comparing the two tables we can see the second one has a subset of the first one. Thus, the following output should be converted so that the structured form of the scan object includes the first table of results only, in addition to the scan details (CLI command, date timestamp, (total) scan tries, and (empty) scan attempts).

```


[H[2J[3J[1;1H[J Currently scanning: Starting.   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: Starting.   |   Screen View: Unique Hosts                 
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts            
                                                                               
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0                 
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
[1;1H[J Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts            
                                                                               
 12 Captured ARP Req/Rep packets, from 8 hosts.   Total size: 504              
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
 192.168.1.16    88:f4:da:1a:b7:65      5     210  Unknown vendor              
 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD 
 192.168.1.3     3c:a3:08:a4:d1:8d      1      42  Texas Instruments           
 192.168.1.2     a8:51:ab:23:c6:49      1      42  Apple, Inc.                 
 192.168.1.4     f8:b9:5a:0a:e3:6c      1      42  LG Innotek                  
 192.168.1.7     cc:c7:60:67:89:48      1      42  Apple, Inc.                 
 192.168.1.8     26:e8:35:b0:a8:79      1      42  Unknown vendor              
 192.168.1.11    00:c0:ca:b9:ae:40      1      42  ALFA, INC.                  
[1;1H[J Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts            
                                                                               
 18 Captured ARP Req/Rep packets, from 9 hosts.   Total size: 756              
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
 192.168.1.16    88:f4:da:1a:b7:65     10     420  Unknown vendor              
 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD 

```

Realistically, the agent should have used TextFSM and NTC Tempaltes to capture something like the json below.

```json
{
    "netdiscover_scan": {
        "scanner": "netdiscover",
        "args": "netdiscover — A — active ARP scan 192.168.1.0/24",
        "start_time": "Tue Jun 23 19:06:27 2026",
        "systems": [
            {
                "ipv4": "192.168.1.16",
                "mac": "88:f4:da:1a:b7:65",
                "mac_vendor": "Unknown vendor",
                "count": 5,
                "len": 210
            },
            {
                "ipv4": "192.168.1.1",
                "mac": "14:5f:94:d8:7a:5f",
                "mac_vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.3",
                "mac": "3c:a3:08:a4:d1:8d",
                "mac_vendor": "Texas Instruments",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.2",
                "mac": "a8:51:ab:23:c6:49",
                "mac_vendor": "Apple, Inc.",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.4",
                "mac": "f8:b9:5a:0a:e3:6c",
                "mac_vendor": "LG Innotek",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.7",
                "mac": "cc:c7:60:67:89:48",
                "mac_vendor": "Apple, Inc.",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.8",
                "mac": "26:e8:35:b0:a8:79",
                "mac_vendor": "Unknown vendor",
                "count": 1,
                "len": 42
            },
            {
                "ipv4": "192.168.1.11",
                "mac": "00:c0:ca:b9:ae:40",
                "mac_vendor": "ALFA, INC.",
                "count": 1,
                "len": 42
            }
        ],
        "runstats": {
            "finished_time": {
                "end_time": "Tue Jun 23 19:06:28 2026",
                "elapsed": 0.42,
                "summary": "NetDiscover done at Tue Jun 23 19:06:28 2026; 8 Systems Discovered, 5 Scan Tries, 3 Empty Scans, scanned in 0.42 seconds",
                "exit_status": "success"
            },
            "systems": {
                "discovered": 8,
                "scan_tries": 5,
                "empty_scans": 3
            }
        }
    }
}
```

When converting the above structured json format into a nodes and edges graph of nuggets, the following concepts must be considered:

- Everything on the network that has some kind of address (ip address, bluethooth address, etc.) is subclass of a `system`
- A `host` is a subclass of a `system` that is a generic computer on the network (e.g. Windows, Linux, macOS, etc.).
- A `device` is a subclass of a `system` that is a specific device on the network (e.g. router, switch, printer, TV, fridge etc.).
- A `mobile` is a subclass of a `system` that is a mobile device on the network (e.g. phone, tablet, etc.).
- A `server` is a subclass of a `system` that is a rack-mounted server on the network (e.g. Windows Server, Linux Server, etc.). It often does not have a screen or keyboard connected to it.

However, initially, when all we know is the mac address vendor it is not possible tto proeprly classify all devices, and so the conversion should make them all into `system` nuggets, since we know insufficient about the systems to classify them.

Obviously, the `system` will contain a `networks` category, which then contains an IP_ADRESS and a MAC_ADDRESS entity, plus a MAC_VENDOR descriptor. This will all be contained by `scan` entity nugget and the descriptor nuggets it has



### Issue 5: Missing Capture of Scan CLI Command and Date Timestamp

You must make sure the CLI command and date timestamp are captured for every scan. This is critical for reproducibility and auditability. Please update your rules to ensure this is captured for every scan, and the examination process should specifically check for these values.
