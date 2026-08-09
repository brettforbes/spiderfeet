# Aircrack-ng CLI Options

Operator reference for the **Aircrack-ng suite 1.7** (Windows zip extract). Prefer airodump CSV/PCAP for SpiderFeet discovery; cracking tools are Linux-first on this host.

| Field | Value |
|-------|-------|
| Suite version | **1.7** |
| Windows binary root | `C:\projects\spiderfeet\.tools\aircrack-ng\aircrack-ng-1.7-win\bin` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_aircrack_help/*.txt` |

> Flags below are from **live help stdout** captured on this host — **do not invent options**.
>
> **airmon-ng:** not present in the official Windows 1.7 zip (Linux/WSL suite component). No Windows help capture.
>
> **aircrack-ng (cracker):** help capture is a **proven limitation** on this host (`The system cannot execute the specified program`). **Do not invent its flags.** Re-capture with Linux `aircrack-ng --help`.

Skill: `.cursor/skills/aircrack-ng/SKILL.md`

---

## SpiderFeet preferred commands

```bash
# Linux/WSL — monitor mode (airmon-ng not in Windows zip)
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Passive survey with parseable CSV (captured airodump-ng flags)
sudo airodump-ng -w survey --output-format csv,pcap wlan0mon
sudo airodump-ng --channel 6 --bssid AA:BB:CC:DD:EE:FF -w wpa wlan0mon

# Injection test / authorized deauth (captured aireplay-ng modes)
sudo aireplay-ng --test wlan0mon
sudo aireplay-ng --deauth 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon

# Decrypt after key known (captured airdecap-ng)
airdecap-ng -e LabNet -p 'passphrase' capture-01.cap

# PMK prep (captured airolib-ng)
airolib-ng pmk_db --import essid essids.txt
airolib-ng pmk_db --import passwd wordlist.txt
airolib-ng pmk_db --batch

# Crack on Linux after re-capturing aircrack-ng --help (not inventing flags here)
# aircrack-ng --help   # Linux/WSL
```

---

## Host facts (this capture)

| Component | Status on this host |
|-----------|---------------------|
| Windows suite extract | `.tools/aircrack-ng/aircrack-ng-1.7-win/` |
| Live help captured | airodump-ng, aireplay-ng, airbase-ng, airdecap-ng, airdecloak-ng, airolib-ng, airtun-ng, airserv-ng, airventriloquist-ng, packetforge-ng, tkiptun-ng, besside-ng, easside-ng, wesside-ng, buddy-ng, makeivs-ng, ivstools, kstats, wpaclean |
| **airmon-ng** | **Not in Windows zip** — Linux/WSL only; no help capture here |
| **aircrack-ng** | Capture failed: `The system cannot execute the specified program` — re-capture on Linux; **do not invent flags** |
| Tools using `-h` not `--help` | airserv-ng, besside-ng, easside-ng, wesside-ng, buddy-ng print usage after rejecting `--` |

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\aircrack-ng\aircrack-ng-1.7-win\bin` on **2026-08-10**. Each block is the full stdout of the listed command (ANSI / stderr noise retained where present).

### aircrack-ng (proven limitation)

Attempted help capture on this host failed. **No flags documented here.** Re-capture on Linux:

```bash
aircrack-ng --help
```

Captured stdout (`.tmp_aircrack_help/aircrack-ng_help.txt`):

```text
The system cannot execute the specified program.
```

### airmon-ng (not in Windows suite)

`airmon-ng` is a **Linux-only** shell helper (monitor-mode wrapper). It is **absent** from the official Windows 1.7 zip. Use Linux/WSL for monitor-mode setup; see [airmon-ng wiki](https://www.aircrack-ng.org/doku.php?id=airmon-ng). No Captured help block on this host.

### airodump-ng (`airodump-ng --help`)

```text
[0m
  Airodump-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: airodump-ng <options> <interface>[,<interface>,...]

  Options:
      --ivs                 : Save only captured IVs
      --gpsd                : Use GPSd
      --write      <prefix> : Dump file prefix
      -w                    : same as --write 
      --beacons             : Record all beacons in dump file
      --update       <secs> : Display update delay in seconds
      --showack             : Prints ack/cts/rts statistics
      -h                    : Hides known stations for --showack
      -f            <msecs> : Time in ms between hopping channels
      --berlin       <secs> : Time before removing the AP/client
                              from the screen when no more packets
                              are received (Default: 120 seconds)
      -r             <file> : Read packets from that file
      -T                    : While reading packets from a file,
                              simulate the arrival rate of them
                              as if they were "live".
      -x            <msecs> : Active Scanning Simulation
      --manufacturer        : Display manufacturer from IEEE OUI list
      --uptime              : Display AP Uptime from Beacon Timestamp
      --wps                 : Display WPS information (if any)
      --output-format
                  <formats> : Output format. Possible values:
                              pcap, ivs, csv, gps, kismet, netxml, logcsv
      --ignore-negative-one : Removes the message that says
                              fixed channel <interface>: -1
      --write-interval
                  <seconds> : Output file(s) write interval in seconds
      --background <enable> : Override background detection.
      -n              <int> : Minimum AP packets recv'd before
                              for displaying it

  Filter options:
      --encrypt   <suite>   : Filter APs by cipher suite
      --netmask <netmask>   : Filter APs by mask
      --bssid     <bssid>   : Filter APs by BSSID
      --essid     <essid>   : Filter APs by ESSID
      --essid-regex <regex> : Filter APs by ESSID using a regular
                              expression
      -a                    : Filter unassociated clients

  By default, airodump-ng hops on 2.4GHz channels.
  You can make it capture on other/specific channel(s) by using:
      --ht20                : Set channel to HT20 (802.11n)
      --ht40-               : Set channel to HT40- (802.11n)
      --ht40+               : Set channel to HT40+ (802.11n)
      --channel <channels>  : Capture on specific channels
      --band <abg>          : Band on which airodump-ng should hop
      -C    <frequencies>   : Uses these frequencies in MHz to hop
      --cswitch  <method>   : Set channel switching method
                    0       : FIFO (default)
                    1       : Round Robin
                    2       : Hop on last
      -s                    : same as --cswitch

      --help                : Displays this usage screen
```

### aireplay-ng (`aireplay-ng --help`)

```text

  Aireplay-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: aireplay-ng <options> <replay interface>

  Filter options:

      -b bssid  : MAC address, Access Point
      -d dmac   : MAC address, Destination
      -s smac   : MAC address, Source
      -m len    : minimum packet length
      -n len    : maximum packet length
      -u type   : frame control, type    field
      -v subt   : frame control, subtype field
      -t tods   : frame control, To      DS bit
      -f fromds : frame control, From    DS bit
      -w iswep  : frame control, WEP     bit
      -D        : disable AP detection

  Replay options:

      -x nbpps  : number of packets per second
      -p fctrl  : set frame control word (hex)
      -a bssid  : set Access Point MAC address
      -c dmac   : set Destination  MAC address
      -h smac   : set Source       MAC address
      -g value  : change ring buffer size (default: 8)
      -F        : choose first matching packet

      Fakeauth attack options:

      -e essid  : set target AP SSID
      -o npckts : number of packets per burst (0=auto, default: 1)
      -q sec    : seconds between keep-alives
      -Q        : send reassociation requests
      -y prga   : keystream for shared key auth
      -T n      : exit after retry fake auth request n time

      Arp Replay attack options:

      -j        : inject FromDS packets

      Fragmentation attack options:

      -k IP     : set destination IP in fragments
      -l IP     : set source IP in fragments

      Test attack options:

      -B        : activates the bitrate test

  Source options:

      -i iface  : capture packets from this interface
      -r file   : extract packets from this pcap file

  Miscellaneous options:

      -R                    : disable /dev/rtc usage
      --ignore-negative-one : if the interface's channel can't be determined,
                              ignore the mismatch, needed for unpatched cfg80211
      --deauth-rc rc        : Deauthentication reason code [0-254] (Default: 7)

  Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)

      --help              : Displays this usage screen
```

### airbase-ng (`airbase-ng --help`)

```text

  Airbase-ng 1.7  - (C) 2008-2022 Thomas d'Otreppe
  Original work: Martin Beck
  https://www.aircrack-ng.org

  usage: airbase-ng <options> <replay interface>

  Options:

      -a bssid         : set Access Point MAC address
      -i iface         : capture packets from this interface
      -w WEP key       : use this WEP key to en-/decrypt packets
      -h MAC           : source mac for MITM mode
      -f disallow      : disallow specified client MACs (default: allow)
      -W 0|1           : [don't] set WEP flag in beacons 0|1 (default: auto)
      -q               : quiet (do not print statistics)
      -v               : verbose (print more messages)
      -A               : Ad-Hoc Mode (allows other clients to peer)
      -Y in|out|both   : external packet processing
      -c channel       : sets the channel the AP is running on
      -X               : hidden ESSID
      -s               : force shared key authentication (default: auto)
      -S               : set shared key challenge length (default: 128)
      -L               : Caffe-Latte WEP attack (use if driver can't send frags)
      -N               : cfrag WEP attack (recommended)
      -x nbpps         : number of packets per second (default: 100)
      -y               : disables responses to broadcast probes
      -0               : set all WPA,WEP,open tags. can't be used with -z & -Z
      -z type          : sets WPA1 tags. 1=WEP40 2=TKIP 3=WRAP 4=CCMP 5=WEP104
      -Z type          : same as -z, but for WPA2
      -V type          : fake EAPOL 1=MD5 2=SHA1 3=auto
      -F prefix        : write all sent and received frames into pcap file
      -P               : respond to all probes, even when specifying ESSIDs
      -I interval      : sets the beacon interval value in ms
      -C seconds       : enables beaconing of probed ESSID values (requires -P)
      -n hex           : User specified ANonce when doing the 4-way handshake

  Filter options:
      --bssid MAC      : BSSID to filter/use
      --bssids file    : read a list of BSSIDs out of that file
      --client MAC     : MAC of client to filter
      --clients file   : read a list of MACs out of that file
      --essid ESSID    : specify a single ESSID (default: default)
      --essids file    : read a list of ESSIDs out of that file

      --help           : Displays this usage screen
```

### airdecap-ng (`airdecap-ng --help`)

```text

  Airdecap-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: airdecap-ng [options] <pcap file>

  Common options:
      -l         : don't remove the 802.11 header
      -b <bssid> : access point MAC address filter
      -e <essid> : target network SSID
      -o <fname> : output file for decrypted packets (default <src>-dec)

  WEP specific option:
      -w <key>   : target network WEP key in hex
      -c <fname> : output file for corrupted WEP packets (default <src>-bad)

  WPA specific options:
      -p <pass>  : target network WPA passphrase
      -k <pmk>   : WPA Pairwise Master Key in hex

      --help     : Displays this usage screen

  If your capture contains any WDS packet, you must specify the -b
  option (otherwise only packets destined to the AP will be decrypted)
```

### airdecloak-ng (`airdecloak-ng --help`)

```text

  Airdecloak-ng 1.7  - (C) 2008-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: airdecloak-ng [options]

  options:

   Mandatory:
     -i <file>             : Input capture file
     --ssid <ESSID>        : ESSID of the network to filter
        or
     --bssid <BSSID>       : BSSID of the network to filter

   Optional:
     -o <file>             : Output packets (valid) file (default: <src>-filtered.pcap)
     -c <file>             : Output packets (cloaked) file (default: <src>-cloaked.pcap)
     -u <file>             : Output packets (unknown/ignored) file (default: invalid_status.pcap)
     --filters <filters>   : Apply filters (separated by a comma). Filters:
           signal:               Try to filter based on signal.
           duplicate_sn:         Remove all duplicate sequence numbers
                                 for both the AP and the client.
           duplicate_sn_ap:      Remove duplicate sequence number for
                                 the AP only.
           duplicate_sn_client:  Remove duplicate sequence number for the
                                 client only.
           consecutive_sn:       Filter based on the fact that IV should
                                 be consecutive (only for AP).
           duplicate_iv:         Remove all duplicate IV.
           signal_dup_consec_sn: Use signal (if available), duplicate and
                                 consecutive sequence number (filtering is
                                  much more precise than using all these
                                  filters one by one).
     --null-packets        : Assume that null packets can be cloaked.
     --disable-base_filter : Do not apply base filter.
     --drop-frag           : Drop fragmented packets

     --help                : Displays this usage screen
```

### airolib-ng (`airolib-ng --help`)

```text

  Airolib-ng 1.7  - (C) 2007, 2008, 2009 ebfe
  https://www.aircrack-ng.org

  Usage: airolib-ng <database> <operation> [options]

  Operations:

       --stats        : Output information about the database.
       --sql <sql>    : Execute specified SQL statement.
       --clean [all]  : Clean the database from old junk. 'all' will also 
                        reduce filesize if possible and run an integrity check.
       --batch        : Start batch-processing all combinations of ESSIDs
                        and passwords.
       --verify [all] : Verify a set of randomly chosen PMKs.
                        If 'all' is given, all invalid PMK will be deleted.

       --import [essid|passwd] <file>   :
                        Import a text file as a list of ESSIDs or passwords.
       --import cowpatty <file>         :
                        Import a cowpatty file.

       --export cowpatty <essid> <file> :
                        Export to a cowpatty file.
```

### airtun-ng (`airtun-ng --help`)

```text

  Airtun-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  Original work: Martin Beck
  https://www.aircrack-ng.org

  usage: airtun-ng <options> <replay interface>

      -x nbpps         : number of packets per second (default: 100)
      -a bssid         : set Access Point MAC address
                         In WDS Mode this sets the Receiver
      -i iface         : capture packets from this interface
      -y file          : read PRGA from this file
      -w wepkey        : use this WEP-KEY to encrypt packets
      -p pass          : use this WPA passphrase to decrypt packets
                         (use with -a and -e)
      -e essid         : target network SSID (use with -p)
      -t tods          : send frames to AP (1) or to client (0)
                         or tunnel them into a WDS/Bridge (2)
      -r file          : read frames out of pcap file
      -h MAC           : source MAC address

  WDS/Bridge Mode options:
      -s transmitter   : set Transmitter MAC address for WDS Mode
      -b               : bidirectional mode. This enables communication
                         in Transmitter's AND Receiver's networks.
                         Works only if you can see both stations.

  Repeater options:
      --repeat         : activates repeat mode
      --bssid <mac>    : BSSID to repeat
      --netmask <mask> : netmask for BSSID filter

      --help           : Displays this usage screen
```

### airserv-ng (`airserv-ng -h  (note: --help rejected; -h works)`)

```text
airserv-ng: unknown option -- -

  Airserv-ng 1.7  - (C) 2007, 2008, 2009 Andrea Bittau
  https://www.aircrack-ng.org

  Usage: airserv-ng <options>

  Options:

       -h         : This help screen
       -p  <port> : TCP port to listen on (default:666)
       -d <iface> : Wifi interface to use
       -c  <chan> : Channel to use
       -v <level> : Debug level (1 to 3; default: 1)
```

### airventriloquist-ng (`airventriloquist-ng --help`)

```text

  Airventriloquist-ng 1.7  - (C) 2015 Tim de Waal
  https://www.aircrack-ng.org

  usage: airventriloquist-ng [options]

      -i <replay interface>   : Interface to listen and inject on
      -d | --deauth           : Send active deauths to encrypted stations
      -e | --essid <value>    : ESSID of target network 
      -p | --passphrase <val> : WPA Passphrase of target network
      -c | --icmp             : Respond to all ICMP frames (Debug)
      -n | --dns              : IP to resolve all DNS queries to
      -s | --hijack <URL>     : URL to look for in HTTP requests
                                <URL> can have wildcards
                                   eg: *jquery*.js*
      -r | --redirect <URL>   : URL to redirect to
      -v | --verbose          : Verbose output
      --help                  : This super helpful message
```

### packetforge-ng (`packetforge-ng --help`)

```text

  Packetforge-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  Original work: Martin Beck
  https://www.aircrack-ng.org

  Usage: packetforge-ng <mode> <options>

  Forge options:

      -p <fctrl>     : set frame control word (hex)
      -a <bssid>     : set Access Point MAC address
      -c <dmac>      : set Destination  MAC address
      -h <smac>      : set Source       MAC address
      -j             : set FromDS bit
      -o             : clear ToDS bit
      -e             : disables WEP encryption
      -k <ip[:port]> : set Destination IP [Port]
      -l <ip[:port]> : set Source      IP [Port]
      -t ttl         : set Time To Live
      -w <file>      : write packet to this pcap file
      -s <size>      : specify size of null packet
      -n <packets>   : set number of packets to generate

  Source options:

      -r <file>      : read packet from this raw file
      -y <file>      : read PRGA from this file

  Modes:

      --arp          : forge an ARP packet    (-0)
      --udp          : forge an UDP packet    (-1)
      --icmp         : forge an ICMP packet   (-2)
      --null         : build a null packet    (-3)
      --custom       : build a custom packet  (-9)

      --help         : Displays this usage screen
```

### tkiptun-ng (`tkiptun-ng --help`)

```text

  Tkiptun-ng 1.7  - (C) 2008-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: tkiptun-ng <options> <replay interface>

  Filter options:

      -d dmac   : MAC address, Destination
      -s smac   : MAC address, Source
      -m len    : minimum packet length (default: 80) 
      -n len    : maximum packet length (default: 80)
      -t tods   : frame control, To      DS bit
      -f fromds : frame control, From    DS bit
      -D        : disable AP detection
      -Z        : select packets manually

  Replay options:

      -x nbpps  : number of packets per second
      -a bssid  : set Access Point MAC address
      -c dmac   : set Destination  MAC address
      -h smac   : set Source       MAC address
      -e essid  : set target AP SSID
      -M sec    : MIC error timeout in seconds [60]

  Debug options:

      -K prga   : keystream for continuation
      -y file   : keystream-file for continuation
      -j        : inject FromDS packets
      -P pmk    : pmk for verification/vuln testing
      -p psk    : psk to calculate pmk with essid

  source options:

      -i iface  : capture packets from this interface
      -r file   : extract packets from this pcap file

      --help    : Displays this usage screen
```

### besside-ng (`besside-ng -h  (note: --help rejected; -h works)`)

```text
besside-ng: unknown option -- -

  Besside-ng 1.7  - (C) 2010 Andrea Bittau
  https://www.aircrack-ng.org

  Usage: /usr/bin/besside-ng [options] <interface>

  Options:

       -b <victim mac>       Victim BSSID
       -R <victim ap regex>  Victim ESSID regex (requires PCRE)
       -s <WPA server>       Upload wpa.cap for cracking
       -c <chan>             chanlock
       -p <pps>              flood rate
       -W                    WPA only
       -v                    verbose, -vv for more, etc.
       -h                    This help screen
```

### easside-ng (`easside-ng -h  (note: --help rejected; -h works)`)

```text
easside-ng: unknown option -- -

  Easside-ng 1.7  - (C) 2007, 2008, 2009 Andrea Bittau
  https://www.aircrack-ng.org

  Usage: easside-ng <options>

  Options:

       -h                : This help screen
       -v   <victim mac> : Victim BSSID
       -m      <src mac> : Source MAC address
       -i           <ip> : Source IP address
       -r    <router ip> : Router IP address
       -s     <buddy ip> : Buddy-ng IP address (mandatory)
       -f        <iface> : Interface to use (mandatory)
       -c      <channel> : Lock card to this channel
       -n                : Determine Internet IP only
```

### wesside-ng (`wesside-ng -h  (note: --help rejected; -h works)`)

```text
wesside-ng: unknown option -- -

  Wesside-ng 1.7  - (C) 2007, 2008, 2009 Andrea Bittau
  https://www.aircrack-ng.org

  Usage: wesside-ng <options>

  Options:

       -h              : This help screen
       -i      <iface> : Interface to use (mandatory)
       -m      <my ip> : My IP address
       -n     <net ip> : Network IP address
       -a      <mymac> : Source MAC Address
       -c              : Do not crack the key
       -p   <min prga> : Minimum bytes of PRGA to gather
       -v <victim mac> : Victim BSSID
       -t  <threshold> : Cracking threshold
       -f   <max chan> : Highest scanned chan (default: 11)
       -k      <txnum> : Ignore acks and tx txnum times
```

### buddy-ng (`buddy-ng -h  (note: --help rejected; -h works)`)

```text
buddy-ng: unknown option -- -

  Buddy-ng 1.7  - (C) 2007,2008 Andrea Bittau
  https://www.aircrack-ng.org

  Usage: buddy-ng <options>

  Options:

       -h        : This help screen
       -p        : Don't drop privileges
```

### makeivs-ng (`makeivs-ng --help`)

```text

  makeivs-ng 1.7  - (C) 2006-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

  usage: makeivs-ng [options]

  Common options:
      -b <bssid> : Set access point MAC address
      -f <num>   : Number of first IV
      -k <key>   : Target network WEP key in hex
      -s <num>   : Seed used to setup random generator
      -w <file>  : Filename to write IVs into
      -c <num>   : Number of IVs to generate
      -d <num>   : Percentage of dupe IVs
      -e <num>   : Percentage of erroneous keystreams
      -l <num>   : Length of keystreams
      -n         : Ignores weak IVs
      -p         : Uses prng algorithm to generate IVs

      --help     : Displays this usage screen
```

### ivstools (`ivstools --help`)

```text

  ivsTools 1.7  - (C) 2006-2022 Thomas d'Otreppe
  https://www.aircrack-ng.org

   usage: ivstools --convert <pcap file> <ivs output file>
        Extract ivs from a pcap file
       ivstools --merge <ivs file 1> <ivs file 2> .. <output file>
        Merge ivs files
```

### kstats (`kstats (usage line)`)

```text
usage: kstats <ivs file> <104-bit key>
```

### wpaclean (`wpaclean (usage line)`)

```text
Usage: /usr/bin/wpaclean <out.cap> <in.cap> [in2.cap] [...]
```

---

## Guardrails

- **Authorized testing only** — wireless interception/injection without permission is illegal in most jurisdictions.
- **Do not invent flags** — especially for `aircrack-ng` until Linux help is captured.
- **airmon-ng** requires Linux/WSL + a monitor-capable adapter.
- Disruptive modes (`aireplay-ng --deauth` / `-0`) only in scoped engagements.

---

## See also

- [Aircrack-ng Zero to Hero](Aircrack-Ng-Zero-to-Hero.md)
- Skill: `.cursor/skills/aircrack-ng/SKILL.md`
- https://www.aircrack-ng.org/doku.php
