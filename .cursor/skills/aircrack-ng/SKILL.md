---
name: aircrack-ng
description: Orchestrate Aircrack-ng suite tools (airmon-ng, airodump-ng, aireplay-ng, aircrack-ng, airbase-ng, airdecap-ng, airolib-ng) for authorized wireless discovery, WPA/WEP capture, and crack workflows. Parse airodump CSV via TextFSM. Use for WiFi OSINT, monitor mode setup, handshake capture, or SpiderFeet WIFI_ACCESS_POINT nugget mapping.
---

# Aircrack-ng — Wireless Scanning and Analysis

## Purpose

Use when an agent must **discover, capture, and analyze WiFi networks** using the [Aircrack-ng](https://www.aircrack-ng.org/) suite on a **monitor-mode-capable** adapter, under **explicit authorization**, then parse results into structured records (airodump CSV → TextFSM → `WIFI_ACCESS_POINT` and related nuggets).

## Step-by-Step Instructions

1. **Confirm authorization** — Written permission for the target airspace and physical location. Unauthorized wireless interception is illegal in most jurisdictions.
2. **Verify adapter** — USB WiFi adapter with monitor mode + packet injection support (see guardrails). Run `iw dev` / `airmon-ng` to list interfaces.
3. **Kill conflicting processes** — `sudo airmon-ng check kill` (or `check` then manual stop) to free the radio.
4. **Enable monitor mode** — `sudo airmon-ng start wlan0` → `wlan0mon` (name varies).
5. **Discover networks** — `sudo airodump-ng wlan0mon` or write CSV: `airodump-ng -w capture --output-format csv wlan0mon`.
6. **Focus target** — Note BSSID, channel, ESSID from CSV; lock channel: `airodump-ng -c <ch> --bssid <MAC> -w wpa_capture wlan0mon`.
7. **Capture handshake (WPA/WPA2)** — Wait for client auth or deauth (authorized pentest only): `aireplay-ng -0 1 -a <AP_BSSID> -c <CLIENT_MAC> wlan0mon`.
8. **Crack (if in scope)** — `aircrack-ng -w wordlist.txt -b <BSSID> wpa_capture-01.cap` or use `airolib-ng` for PMK precomputation.
9. **Parse output** — TextFSM templates on airodump `.csv` files (see `output-and-parsing.md`).
10. **Teardown** — `sudo airmon-ng stop wlan0mon`; restore managed mode.

## If/Then Decision Rules

| If | Then |
|----|------|
| No monitor-capable adapter | Stop — report hardware requirement |
| `airmon-ng check` shows NetworkManager/wpa_supplicant conflict | `check kill` or stop services before monitor mode |
| WPA network, no handshake after passive wait | Authorized test: targeted deauth with `aireplay-ng -0`; else continue passive or move on |
| WEP network (legacy) | Follow WEP workflow: IV collection + ARP replay (`aireplay-ng -3`) |
| Hidden ESSID | Capture probe responses; `aireplay-ng` probe or wait for client traffic |
| Channel hopping misses AP | Fix channel with `-c` on airodump |
| Multiple APs same ESSID | Disambiguate by BSSID in all commands |
| Need decrypted PCAP | `airdecap-ng -e <ESSID> -p <key> input.cap` after key recovered |
| Large WPA dictionary crack | Precompute PMKs: `airolib-ng` import/generate/crack |
| Clientless WEP | See official "no wireless clients" tutorial path |
| Only discovery (OSINT) | Stop after airodump CSV parse — no injection required |

## Guardrails & Pitfalls

- **Authorized testing only** — Own lab, written pentest scope, or explicit SSID/BSSID allow-list.
- **Compatible adapter required** — On-board laptop WiFi often lacks monitor mode/injection; use supported chipsets (e.g. Atheros AR9271, Ralink RT3070, many Alfa USB models). Verify with `airmon-ng start` before planning workflows.
- **Deauth/disruptive attacks** — `aireplay-ng -0` denies service to clients; only in scoped engagements.
- **Legal capture** — Recording third-party traffic without consent may violate wiretap laws.
- **Channel regulatory domain** — Stay within allowed frequencies for your jurisdiction.
- **Driver quirks** — Interface may be `wlan0mon` vs `wlan0`; always use `iw dev` / `airmon-ng` output names.
- **CSV timing** — airodump CSV updates periodically; copy file while airodump running or use `-w` prefix consistently.
- **Do not crack by default in SpiderFeet OSINT** — Discovery/mapping is passive-friendly; cracking is operator opt-in.
- **WEP** — Deprecated encryption; document only for legacy lab assessments.

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md) for adaptive sequences (discovery → focus → capture → crack → decrypt).

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options-by-module.md` | Per-tool flags |
| `workflows.md` | WPA and WEP orchestration |
| `output-and-parsing.md` | airodump CSV TextFSM |
| `nugget-mapping.md` | WiFi findings → nuggets |
| `tactics.md` | Adaptive wireless sequences |
| `sources.md` | Official docs and tutorials |

## Examples

### List interfaces and start monitor mode

```bash
sudo airmon-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### Passive survey (all channels)

```bash
sudo airodump-ng wlan0mon
```

### Survey with CSV for parsing

```bash
sudo airodump-ng -w survey --output-format csv,pcap wlan0mon
# Produces survey-01.csv, survey-01.cap
```

### Lock AP and capture WPA handshake

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wpa_handshake wlan0mon
# second terminal (authorized only):
sudo aireplay-ng -0 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

### Crack WPA with wordlist

```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF wpa_handshake-01.cap
```

### WEP IV capture + ARP replay

```bash
sudo airodump-ng -c 1 --bssid AA:BB:CC:DD:EE:FF -w wep_capture wlan0mon
sudo aireplay-ng -3 -b AA:BB:CC:DD:EE:FF -h 11:22:33:44:55:66 wlan0mon
aircrack-ng wep_capture-01.cap
```

### airolib-ng PMK database

```bash
airolib-ng pmk_db --import essid /tmp/essids.txt
airolib-ng pmk_db --import passwd /tmp/wordlist.txt
airolib-ng pmk_db --clean all
airolib-ng pmk_db --batch
aircrack-ng -r pmk_db -b AA:BB:CC:DD:EE:FF capture.cap
```

### Decrypt capture after key known

```bash
airdecap-ng -e "LabNetwork" -p "s3cretkey" encrypted.cap
```

### Stop monitor mode

```bash
sudo airmon-ng stop wlan0mon
```
