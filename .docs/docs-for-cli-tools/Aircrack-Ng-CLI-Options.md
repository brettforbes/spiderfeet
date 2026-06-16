# Aircrack-ng CLI Options

Operator quick reference for the Aircrack-ng suite. Per-module detail: `.cursor/skills/aircrack-ng/references/cli-options-by-module.md`.

> Run `<tool> --help` on your system for authoritative syntax.

---

## airmon-ng

| Command | Description |
|---------|-------------|
| `airmon-ng` | List interfaces |
| `airmon-ng start <iface> [ch]` | Monitor mode on |
| `airmon-ng stop <ifacemon>` | Monitor mode off |
| `airmon-ng check` | List blocking processes |
| `airmon-ng check kill` | Kill blockers |

---

## airodump-ng

| Flag | Description |
|------|-------------|
| `<iface>` | Monitor interface |
| `-c <ch>` | Fixed channel |
| `--bssid <mac>` | Filter AP |
| `-w <prefix>` | Output prefix |
| `--output-format csv,pcap` | Output types |
| `-a` | Associated clients only |
| `--manufacturer` | OUI vendor |
| `-d <ms>` | Hop delay |
| `--ignore-negative-one` | Ignore ch -1 |

```bash
sudo airodump-ng -w scan --output-format csv,pcap wlan0mon
sudo airodump-ng -c 11 --bssid AA:BB:CC:DD:EE:FF -w cap wlan0mon
```

---

## aireplay-ng

| Flag | Description |
|------|-------------|
| `-0 <n>` | Deauthentication |
| `-1 <delay>` | Fake authentication |
| `-3` | ARP replay (WEP) |
| `-4` | Chopchop (WEP) |
| `-5` | Fragmentation (WEP) |
| `-6` | Caffe Latte |
| `-9` | Injection test |
| `-a <bssid>` | AP MAC |
| `-c <mac>` | Client MAC |
| `-e <essid>` | ESSID |
| `-h <mac>` | Source MAC |

```bash
sudo aireplay-ng -9 wlan0mon
sudo aireplay-ng -0 3 -a AP -c CLIENT wlan0mon
sudo aireplay-ng -3 -b AP -h CLIENT wlan0mon
```

---

## aircrack-ng

| Flag | Description |
|------|-------------|
| `<file.cap>` | Capture file |
| `-b <bssid>` | Target BSSID |
| `-e <essid>` | Target ESSID |
| `-w <wordlist>` | WPA dictionary |
| `-r <airolib>` | PMK database |
| `-a 1` / `-a 2` | Force WEP / WPA |
| `-p <cpus>` | CPU threads |
| `-q` | Quiet |

```bash
aircrack-ng -b AP_MAC -w wordlist.txt capture-01.cap
aircrack-ng -r pmk_db -b AP_MAC capture-01.cap
```

---

## airdecap-ng

| Flag | Description |
|------|-------------|
| `-e <essid>` | Network name |
| `-p <pass>` | WPA passphrase |
| `-w <hex>` | WEP key |

```bash
airdecap-ng -e LabNet -p secret capture.cap
```

---

## airolib-ng

| Subcommand | Description |
|------------|-------------|
| `<db> --import essid <file>` | Import ESSIDs |
| `<db> --import passwd <file>` | Import passwords |
| `<db> --clean all` | Clean DB |
| `<db> --batch` | Precompute PMKs |
| `<db> --stats` | Statistics |

---

## airbase-ng

| Flag | Description |
|------|-------------|
| `-e <essid>` | AP name |
| `-c <ch>` | Channel |
| `-W 0\|1` | Open / WEP |

```bash
sudo airbase-ng -e RogueLab -c 6 wlan0mon
```

---

## airgraph-ng

| Flag | Description |
|------|-------------|
| `-i <csv>` | Input CSV |
| `-o <png>` | Output image |
| `-a` | AP graph |
| `-c` | Client graph |

---

## Utility tools

| Tool | Purpose |
|------|---------|
| `wpaclean` | Extract clean handshake cap |
| `ivstools` | IV extraction |
| `packetforge-ng` | Craft WEP packets |
| `airdecloak-ng` | WEP decloak |
| `airdrop-ng` | Client redirection rules |

---

## Typical command chains

### Passive survey

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo airodump-ng -w survey --output-format csv wlan0mon
sudo airmon-ng stop wlan0mon
```

### WPA capture + crack

```bash
sudo airodump-ng -c 6 --bssid AP -w wpa wlan0mon
# optional authorized deauth:
sudo aireplay-ng -0 2 -a AP -c CLIENT wlan0mon
aircrack-ng -w wordlist.txt -b AP wpa-01.cap
```

---

## Guardrails

- **Authorized testing only**
- **Compatible adapter required** (monitor + injection verified with `aireplay-ng -9`)
- Disruptive attacks (`-0` deauth) only in scoped engagements

---

## See also

- [Aircrack-ng Zero to Hero](Aircrack-Ng-Zero-to-Hero.md)
- https://www.aircrack-ng.org/doku.php
