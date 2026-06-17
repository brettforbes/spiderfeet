# Aircrack-ng CLI Options by Module

Per-tool flags for the [Aircrack-ng suite](https://www.aircrack-ng.org/). Run `<tool> --help` on the target system for authoritative syntax.

---

## airmon-ng

Manage monitor mode on wireless interfaces.

| Command / flag | Description |
|----------------|-------------|
| `airmon-ng` | List interfaces and driver/chipset |
| `airmon-ng start <iface>` | Start monitor mode on interface |
| `airmon-ng start <iface> <channel>` | Start on fixed channel |
| `airmon-ng stop <iface>mon` | Stop monitor mode |
| `airmon-ng check` | List processes that interfere with monitor mode |
| `airmon-ng check kill` | Kill interfering processes (NetworkManager, wpa_supplicant, etc.) |

**Notes:** Resulting monitor iface often `wlan0mon` but naming is driver-dependent.

---

## airodump-ng

802.11 packet capture, AP/client discovery, CSV logging.

| Flag | Description |
|------|-------------|
| `<interface>` | Monitor mode interface (positional) |
| `-c <channel>` | Fixed channel (1–14 2.4 GHz; 5 GHz channel numbers for dual-band) |
| `--band <a\|bg\|abg\|bg>` | Restrict band |
| `--bssid <MAC>` | Filter to AP BSSID |
| `-w <prefix>` | Output file prefix (`-01.cap`, `-01.csv`, …) |
| `--output-format <csv,pcap,ivs,csv,pcap>` | Comma-separated output types |
| `--write-interval <sec>` | CSV flush interval |
| `-a` | Only show associated clients |
| `--showack` | Print ACK/CTS/RTS statistics |
| `-m` | Hide unassociated clients |
| `-n <min packets>` | Minimum packet count to display AP |
| `-N` | WEP detection filter |
| `-d <msec>` | Channel hop delay |
| `-H` | Hide IEEE 802.11 headers in dump |
| `-D` | WDS nodes |
| `-s` | Measure beacon strength (last beacon) |
| `-h` | Hides known APs (ESSID probe) |
| `-u <sec>` | Time before declaring AP inactive |
| `--ignore-negative-one` | Ignore -1 channel (driver quirk) |
| `--manufacturer` | Show manufacturer from OUI |
| `--beacons` | Record all beacons in cap |
| `-R` | Assume all frames WPA length (rare) |
| `-x <mB>` | Active scanning bitrate |
| `-M` | Display MAN vs UNK authentication |
| `-B` | Do not show APs (clients only) — rare |
| `-K` | WEP key in ASCII (debug) |
| `-f <MHz>` | Frequency instead of channel |

**Common invocations:**

```bash
airodump-ng wlan0mon
airodump-ng -c 11 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
airodump-ng -w survey --output-format csv,pcap wlan0mon
```

---

## aireplay-ng

Frame injection: deauth, fake auth, ARP replay, chopchop, etc.

| Flag | Description |
|------|-------------|
| `<interface>` | Monitor mode interface |
| `-0 <count>` | Deauthentication attack (count frames; 0 = stream) |
| `-1 <delay>` | Fake authentication with delay |
| `-2` | Interactive packet replay |
| `-3` | ARP request replay (WEP IV generation) |
| `-4` | KoreK chopchop attack (WEP) |
| `-5` | Fragmentation attack (WEP) |
| `-6` | caffe-latte attack (WEP, clientless) |
| `-7` | Clientless fragmentation (WEP) |
| `-8` | QoS null replay |
| `-9` | Injection test |
| `-a <BSSID>` | AP MAC |
| `-c <MAC>` | Client MAC (source for deauth) |
| `-h <MAC>` | Source MAC for injected frames |
| `-e <ESSID>` | Target ESSID (fake auth) |
| `-D` | Disable AP detection |
| `-j` | ARP replay from DS |
| `-g <packets>` | Change ring buffer size |
| `-F` | Choose first matching packet |
| `-B` | AP MAC from packet |
| `-d <delay>` | Delay between packets (ms) |
| `-f <packets/sec>` | Rate |
| `-x <pps>` | Packets per second |
| `-p <nb>` | Number of packets to send |
| `-o <nb>` | Starting packet # |
| `-k <IP>` | Dest IP for ARP replay |
| `-l <IP>` | Source IP for ARP replay |
| `-t <ttl>` | TTL |
| `-s <size>` | Packet size |
| `-n <nbpps>` | Packets per burst |
| `-m <rate>` | Rate in Mbps |
| `-r <file>` | Pcap to replay |

**Examples:**

```bash
aireplay-ng -0 5 -a AP_MAC -c CLIENT_MAC wlan0mon
aireplay-ng -1 0 -e LabNet -a AP_MAC -h MY_MAC wlan0mon
aireplay-ng -3 -b AP_MAC -h CLIENT_MAC wlan0mon
```

---

## aircrack-ng

WEP/WPA-PSK key recovery from captures.

| Flag | Description |
|------|-------------|
| `<capture.cap>` | PCAP/IVS file(s) |
| `-a <mode>` | Force mode: `1`=WEP, `2`=WPA-PSK |
| `-b <BSSID>` | Target AP BSSID |
| `-e <ESSID>` | Target ESSID |
| `-w <wordlist>` | Wordlist file for WPA |
| `-r <airolib_db>` | airolib-ng database for PMK lookup |
| `-p <nbcpu>` | CPU count |
| `-q` | Quiet |
| `-C <macs>` | Merge APs (WEP) |
| `-l <file>` | Log key to file |
| `-E <file>` | Session file |
| `-J <file>` | WPA session file |
| `-S` | WPA speed test |
| `-Z <sec>` | WPA length brute force (discouraged) |
| `-M <num>` | WEP key index |
| `-d <debug>` | Debug mask |
| `-V` | Verbose |
| `-K` | WEP key in ASCII |
| `-D` | WEP decloak |
| `-y <file>` | KoreK optimized WEP |
| `-0` | WEP attack mode 0 (PTW) |
| `-1` | WEP attack mode 1 (FMS) |
| `-n <bits>` | WEP key length (64/128) |
| `-m <idx>` | WEP key index |
| `-f <factor>` | WEP fudge factor |
| `-x <nb>` | WEP last IVs |
| `-k <key>` | WEP 10-byte key |
| `-H` | KoreK WEP |
| `-R` | WEP testing |

**Examples:**

```bash
aircrack-ng -b AA:BB:CC:DD:EE:FF -w wordlist.txt capture-01.cap
aircrack-ng -r pmk_db -b AA:BB:CC:DD:EE:FF capture-01.cap
aircrack-ng wep-01.cap
```

---

## airbase-ng

Soft AP / honeypot for lab testing.

| Flag | Description |
|------|-------------|
| `-e <ESSID>` | AP ESSID |
| `-c <channel>` | Channel |
| `-P` | Send beacon probes |
| `-A` | Ad-hoc mode |
| `-C <seconds>` | Beacon interval |
| `-W 0\|1` | WEP: 0=open, 1=WEP |
| `-N` | No beacon flood |
| `-x <pps>` | Packets per second |
| `-s` | Shared key authentication |
| `-S` | Hide SSID |
| `-L` | Caffe Latte WEP attack |
| `-Y <file>` | WEP key file |
| `-d` | All clients |
| `-z <type>` | WPA type |
| `-Z <type>` | WPA2 type |
| `-V <mode>` | Validation mode |
| `-F <prefix>` | MAC filter prefix |
| `-w <file>` | Write packet capture |
| `-D` | Do not respond to probes |
| `-I <interval>` | Beacon interval ms |
| `-C` | Beacon count |

```bash
airbase-ng -e RogueAP -c 6 wlan0mon
```

---

## airdecap-ng

Decrypt WEP/WPA captures with known key.

| Flag | Description |
|------|-------------|
| `<input.cap>` | Encrypted capture |
| `-l <file>` | Output decrypted pcap |
| `-e <ESSID>` | Network name |
| `-p <pass>` | WPA passphrase |
| `-w <hexkey>` | WEP hex key |
| `-t <num>` | Key type |
| `-k <index>` | WEP key index |

```bash
airdecap-ng -e LabNet -p secretpass encrypted.cap
```

---

## airdecloak-ng

Remove WEP cloaking (hidden WEP).

| Flag | Description |
|------|-------------|
| `-i <in>` | Input cap |
| `-o <out>` | Output cap |
| `-d <debug>` | Debug level |

---

## airolib-ng

PMK database for faster WPA cracking.

| Subcommand | Description |
|------------|-------------|
| `<db> --import essid <file>` | Import ESSIDs |
| `<db> --import passwd <file>` | Import passwords |
| `<db> --clean all` | Remove invalid entries |
| `<db> --batch` | Precompute all PMKs |
| `<db> --verify all` | Verify database |
| `<db> --stats` | Statistics |
| `<db> --export <out>` | Export |
| `<db> --sql <query>` | SQL query |

Used with `aircrack-ng -r <db>`.

---

## airdrop-ng

Rule-based wireless client redirection (specialized).

| Flag | Description |
|------|-------------|
| `-i <iface>` | Interface |
| `-r <rules>` | Rules file |
| `-b <file>` | Blacklist |
| `-w <file>` | Whitelist |
| `-d` | Disable DSA |
| `-s <MAC>` | Source MAC |
| `-h` | Help |

---

## airgraph-ng

Graph AP/client relationships from airodump CSV.

| Flag | Description |
|------|-------------|
| `-i <csv>` | Input airodump CSV |
| `-o <png>` | Output graph |
| `-a` | AP graph |
| `-c` | Client graph |
| `-l` | Load balancing view |

---

## besside-ng / easside-ng / wesside-ng

Automated WEP/WPA attack tools (legacy/lab). Prefer explicit `airodump` + `aireplay` + `aircrack` for controlled engagements.

| Tool | Purpose |
|------|---------|
| `besside-ng` | Auto WEP/WPA capture and crack attempt |
| `easside-ng` | WEP via WDS tunnel (legacy) |
| `wesside-ng` | Automated WEP cracking |

Use only in isolated lab environments with authorization.

---

## packetforge-ng

Craft encrypted packets for WEP injection.

| Flag | Description |
|------|-------------|
| `-a <BSSID>` | AP MAC |
| `-h <MAC>` | Source MAC |
| `-k <key>` | WEP key |
| `-l <len>` | Packet length |
| `-y <file>` | PRGA file |
| `-w <out>` | Output file |

---

## ivstools / makeivs-ng / wpaclean

| Tool | Purpose |
|------|---------|
| `ivstools` | Extract IVs from pcap |
| `makeivs-ng` | Build IVS file |
| `wpaclean` | Strip WPA handshakes from large pcaps |

```bash
wpaclean clean.cap noisy_capture.cap
```

---

## Suite-wide prerequisites

| Requirement | Check |
|-------------|-------|
| Monitor mode | `airmon-ng start wlan0` succeeds |
| Injection | `aireplay-ng -9 wlan0mon` |
| Root | Most tools require `sudo` |
| Compatible driver | `airmon-ng` lists chipset/driver |

See [workflows.md](workflows.md) for orchestration.
