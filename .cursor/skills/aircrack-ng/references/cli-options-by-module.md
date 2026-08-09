# Aircrack-ng CLI Options by Module

Flags below are summarized from **live Captured help** on **2026-08-10** (`.tmp_aircrack_help/`). Full verbatim blocks: [Aircrack-Ng-CLI-Options.md](../../../.docs/docs-for-cli-tools/Aircrack-Ng-CLI-Options.md).

**Do not invent flags.** Especially for `aircrack-ng` (cracker) — no successful help on this host.

| Tool | Capture status |
|------|----------------|
| airmon-ng | **Not in Windows zip** — Linux/WSL; see wiki |
| aircrack-ng | **Proven limitation** — `The system cannot execute the specified program` |
| Others below | Captured from Windows 1.7 suite |

---

## airmon-ng (Linux/WSL only)

Not present in the official Windows 1.7 zip. No Captured help on this host.

Typical Linux operations (wiki / suite docs — re-verify with `airmon-ng` on Linux):

```bash
sudo airmon-ng
sudo airmon-ng check
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo airmon-ng stop wlan0mon
```

Wiki: https://www.aircrack-ng.org/doku.php?id=airmon-ng

---

## aircrack-ng (proven limitation)

Help capture failed on this host. **No flag table.** Re-capture:

```bash
# Linux / WSL
aircrack-ng --help
```

Captured error (`.tmp_aircrack_help/aircrack-ng_help.txt`):

```text
The system cannot execute the specified program.
```

---

## airodump-ng

`usage: airodump-ng <options> <interface>[,<interface>,...]`

| Flag | Description (from help) |
|------|-------------------------|
| `--ivs` | Save only captured IVs |
| `--gpsd` | Use GPSd |
| `--write` / `-w` `<prefix>` | Dump file prefix |
| `--beacons` | Record all beacons in dump file |
| `--update` `<secs>` | Display update delay |
| `--showack` | ACK/CTS/RTS statistics |
| `-h` | Hide known stations for `--showack` |
| `-f` `<msecs>` | Time between hopping channels |
| `--berlin` `<secs>` | Remove AP/client from screen when quiet (default 120) |
| `-r` `<file>` | Read packets from file |
| `-T` | Simulate live arrival when reading file |
| `-x` `<msecs>` | Active Scanning Simulation |
| `--manufacturer` | Display manufacturer from IEEE OUI list |
| `--uptime` | Display AP uptime from beacon timestamp |
| `--wps` | Display WPS information |
| `--output-format` `<formats>` | `pcap`, `ivs`, `csv`, `gps`, `kismet`, `netxml`, `logcsv` |
| `--ignore-negative-one` | Suppress fixed channel -1 message |
| `--write-interval` `<seconds>` | Output write interval |
| `--background` `<enable>` | Override background detection |
| `-n` `<int>` | Minimum AP packets before display |
| `--encrypt` `<suite>` | Filter APs by cipher suite |
| `--netmask` `<netmask>` | Filter APs by mask |
| `--bssid` `<bssid>` | Filter APs by BSSID |
| `--essid` `<essid>` | Filter APs by ESSID |
| `--essid-regex` `<regex>` | Filter APs by ESSID regex |
| `-a` | Filter unassociated clients |
| `--ht20` / `--ht40-` / `--ht40+` | 802.11n channel width |
| `--channel` `<channels>` | Capture on specific channels |
| `--band` `<abg>` | Band to hop |
| `-C` `<frequencies>` | Hop these MHz frequencies |
| `--cswitch` / `-s` `<method>` | Channel switch: 0 FIFO, 1 Round Robin, 2 Hop on last |
| `--help` | Usage |

```bash
airodump-ng -w survey --output-format csv,pcap wlan0mon
airodump-ng --channel 11 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## aireplay-ng

`usage: aireplay-ng <options> <replay interface>`

**Filter:** `-b` bssid, `-d` dmac, `-s` smac, `-m`/`-n` len, `-u` type, `-v` subt, `-t` tods, `-f` fromds, `-w` iswep, `-D` disable AP detection.

**Replay:** `-x` nbpps, `-p` fctrl, `-a` bssid, `-c` dmac, `-h` smac, `-g` ring, `-F` first match.

**Fakeauth:** `-e` essid, `-o` npckts, `-q` sec, `-Q` reassoc, `-y` prga, `-T` n.

**ARP replay:** `-j` FromDS.

**Fragmentation:** `-k`/`-l` IP.

**Test:** `-B` bitrate test.

**Source:** `-i` iface, `-r` file.

**Misc:** `-R`, `--ignore-negative-one`, `--deauth-rc` rc.

**Attack modes** (numbers still work):

| Long | Short | Role |
|------|-------|------|
| `--deauth` count | `-0` | Deauthenticate stations |
| `--fakeauth` delay | `-1` | Fake authentication |
| `--interactive` | `-2` | Interactive frame selection |
| `--arpreplay` | `-3` | ARP-request replay |
| `--chopchop` | `-4` | Chopchop WEP |
| `--fragment` | `-5` | Keystream generation |
| `--caffe-latte` | `-6` | Client IV query |
| `--cfrag` | `-7` | Fragments against client |
| `--migmode` | `-8` | WPA migration mode |
| `--test` | `-9` | Injection test |

```bash
aireplay-ng --test wlan0mon
aireplay-ng --deauth 3 -a AP_MAC -c CLIENT_MAC wlan0mon
aireplay-ng --arpreplay -b AP_MAC -h CLIENT_MAC wlan0mon
```

---

## airdecap-ng

`usage: airdecap-ng [options] <pcap file>`

| Flag | Description |
|------|-------------|
| `-l` | Don't remove 802.11 header |
| `-b` `<bssid>` | AP MAC filter (required for WDS in capture) |
| `-e` `<essid>` | Target SSID |
| `-o` `<fname>` | Decrypted output (default `<src>-dec`) |
| `-w` `<key>` | WEP key hex |
| `-c` `<fname>` | Corrupted WEP packets (default `<src>-bad`) |
| `-p` `<pass>` | WPA passphrase |
| `-k` `<pmk>` | WPA PMK hex |
| `--help` | Usage |

```bash
airdecap-ng -e LabNet -p secret capture.cap
```

---

## airolib-ng

`Usage: airolib-ng <database> <operation> [options]`

| Operation | Description |
|-----------|-------------|
| `--stats` | Database info |
| `--sql` `<sql>` | Execute SQL |
| `--clean` `[all]` | Clean junk; `all` also reduce size + integrity check |
| `--batch` | Batch-process ESSID×password PMKs |
| `--verify` `[all]` | Verify random PMKs; `all` deletes invalid |
| `--import essid\|passwd` `<file>` | Import text lists |
| `--import cowpatty` `<file>` | Import cowpatty |
| `--export cowpatty` `<essid>` `<file>` | Export cowpatty |

```bash
airolib-ng pmk_db --import essid essids.txt
airolib-ng pmk_db --import passwd wordlist.txt
airolib-ng pmk_db --batch
```

---

## airbase-ng

`usage: airbase-ng <options> <replay interface>`

Key options from help: `-a` bssid, `-i` iface, `-w` WEP key, `-h` MAC, `-f` disallow, `-W` 0\|1, `-q`/`-v`, `-A` Ad-Hoc, `-Y` in\|out\|both, `-c` channel, `-X` hidden ESSID, `-s`/`-S` shared key, `-L` Caffe-Latte, `-N` cfrag, `-x` nbpps, `-y` no broadcast probes, `-0` all tags, `-z`/`-Z` WPA/WPA2 type, `-V` fake EAPOL, `-F` prefix, `-P`, `-I` interval, `-C` seconds, `-n` hex ANonce; filters `--bssid`, `--bssids`, `--client`, `--clients`, `--essid`, `--essids`.

```bash
airbase-ng --essid RogueLab -c 6 wlan0mon
```

---

## airdecloak-ng

Mandatory: `-i` `<file>`, and `--ssid` **or** `--bssid`. Optional: `-o`/`-c`/`-u` outputs, `--filters`, `--null-packets`, `--disable-base_filter`, `--drop-frag`.

---

## airtun-ng

`usage: airtun-ng <options> <replay interface>`

`-x` nbpps, `-a` bssid, `-i` iface, `-y` PRGA file, `-w` wepkey, `-p` passphrase (+ `-a`/`-e`), `-e` essid, `-t` tods, `-r` file, `-h` MAC; WDS `-s`/`-b`; repeater `--repeat`, `--bssid`, `--netmask`.

---

## airserv-ng

Use `-h` (not `--help`). Options: `-p` port (default 666), `-d` iface, `-c` chan, `-v` level.

---

## packetforge-ng

`Usage: packetforge-ng <mode> <options>`

Forge: `-p` fctrl, `-a`/`-c`/`-h` MACs, `-j` FromDS, `-o` clear ToDS, `-e` disable WEP, `-k`/`-l` ip[:port], `-t` ttl, `-w` file, `-s` size, `-n` packets; source `-r`/`-y`. Modes: `--arp` (`-0`), `--udp` (`-1`), `--icmp` (`-2`), `--null` (`-3`), `--custom` (`-9`).

---

## tkiptun-ng

Filter/replay/debug options per Captured help (`-d`/`-s`/`-m`/`-n`/`-t`/`-f`/`-D`/`-Z`, `-x`/`-a`/`-c`/`-h`/`-e`/`-M`, `-K`/`-y`/`-j`/`-P`/`-p`, `-i`/`-r`).

---

## besside-ng / easside-ng / wesside-ng / buddy-ng

Use `-h` for usage ( `--` rejected on capture). See Captured help for full option lists (victim BSSID, channel lock, buddy IP, etc.).

---

## airventriloquist-ng

`-i` iface, `-d`/`--deauth`, `-e`/`--essid`, `-p`/`--passphrase`, `-c`/`--icmp`, `-n`/`--dns`, `-s`/`--hijack`, `-r`/`--redirect`, `-v`/`--verbose`.

---

## Helpers

| Tool | Captured usage |
|------|----------------|
| `ivstools` | `--convert <pcap> <ivs>`; `--merge <ivs…> <out>` |
| `makeivs-ng` | `-b`/`-f`/`-k`/`-s`/`-w`/`-c`/`-d`/`-e`/`-l`/`-n`/`-p` |
| `kstats` | `kstats <ivs file> <104-bit key>` |
| `wpaclean` | `wpaclean <out.cap> <in.cap> [in2.cap …]` |

```bash
wpaclean clean.cap noisy-01.cap
ivstools --convert capture.cap out.ivs
```
