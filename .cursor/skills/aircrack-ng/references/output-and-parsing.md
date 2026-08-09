# Aircrack-ng Output and Parsing

## airodump-ng output files

With `-w <prefix>`:

| File | Contents |
|------|----------|
| `<prefix>-01.cap` | 802.11 PCAP |
| `<prefix>-01.csv` | AP and client tables (primary parse target) |
| `<prefix>-01.kismet.csv` | Kismet-compatible CSV (if enabled) |
| `<prefix>-01.log.csv` | GPS log (if GPS linked) |

Use `--output-format csv,pcap` for SpiderFeet-friendly discovery (formats from Captured airodump-ng help: `pcap`, `ivs`, `csv`, `gps`, `kismet`, `netxml`, `logcsv`).

---

## CSV structure

airodump-ng CSV has **two sections** in one file:

1. **AP list** — starts after header row `BSSID, First time seen, ...`
2. **Station list** — separated by blank lines and header `Station MAC, First time seen, ...`

Between sections you may see blank lines and `BSSID,Station` client mapping rows.

### AP table columns (typical)

| Column | Example | Notes |
|--------|---------|-------|
| BSSID | `AA:BB:CC:DD:EE:FF` | AP MAC |
| First time seen | timestamp | |
| Last time seen | timestamp | |
| channel | `6` | |
| Speed | `270` | |
| Privacy | `WPA2` | `OPN`, `WEP`, `WPA`, `WPA2`, `WPA3` |
| Cipher | `CCMP` | |
| Authentication | `PSK` | |
| Power | `-42` | dBm |
| beacons | count | |
| # IV | count | WEP IVs |
| LAN IP | `0.0.0.0` | Often empty |
| ID-length | ESSID length | |
| ESSID | `CorpWiFi` | `<length: 0>` if hidden |
| Key | | Usually empty |

### Station (client) table columns (typical)

| Column | Example |
|--------|---------|
| Station MAC | `11:22:33:44:55:66` |
| First time seen | |
| Last time seen | |
| Power | |
| # packets | |
| BSSID | Associated AP |
| Probed ESSIDs | `Guest,CorpWiFi` |

---

## Parsing challenges

| Issue | Handling |
|-------|----------|
| Multi-section file | Split on station header or parse statefully in TextFSM |
| Hidden ESSID | `ESSID` shows length placeholder; use BSSID as key |
| Commas in ESSID | Rare; CSV may quote fields — prefer robust split |
| File locked while writing | Copy to temp path or use `--write-interval` |
| Channel `-1` | Driver quirk; `--ignore-negative-one` on capture |

---

## TextFSM template: AP rows (excerpt)

Use with `.cursor/skills/textfsm/` patterns.

```
Value Required BSSID ([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})
Value FIRST_SEEN (.+?)
Value LAST_SEEN (.+?)
Value CHANNEL (\d+)
Value SPEED (\d+)
Value PRIVACY (\S+)
Value CIPHER (\S+)
Value AUTH (\S+)
Value POWER (-?\d+)
Value BEACONS (\d+)
Value IV (\d+)
Value ESSID (.+)

Start
  ^BSSID,\s*First time seen
  ^${BSSID},\s*${FIRST_SEEN},\s*${LAST_SEEN},\s*${CHANNEL},\s*${SPEED},\s*${PRIVACY},\s*${CIPHER},\s*${AUTH},\s*${POWER},\s*${BEACONS},\s*${IV},\s*[^,]*,\s*[^,]*,\s*${ESSID}\s*$$ -> Record
  ^Station MAC -> Stations
```

### Stations state (excerpt)

```
Value Required STATION_MAC ([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})
Value AP_BSSID ([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})
Value PROBED_ESSIDS (.+)

Stations
  ^${STATION_MAC},\s*[^,]*,\s*[^,]*,\s*[^,]*,\s*[^,]*,\s*${AP_BSSID}.* -> Record
```

Validate against real `survey-01.csv` fixtures before production use.

---

## Python parse sketch

```python
import textfsm
from pathlib import Path

def parse_airodump_csv(raw: str) -> dict:
    ap_tmpl = Path("airodump_ap.textfsm")
    st_tmpl = Path("airodump_station.textfsm")
    # Split sections if single template is awkward
    ap_section, _, st_section = raw.partition("Station MAC")
    with ap_tmpl.open() as f:
        aps = textfsm.TextFSM(f).ParseTextToDicts(ap_section)
  # ... stations similarly
    return {"access_points": aps, "stations": stations}
```

For JSON-native pipelines, consider `tshark -T fields` on PCAP as alternative when PCAP is primary artifact.

---

## aircrack-ng stdout

**Note:** On this Windows host, `aircrack-ng` help/execution is a **proven limitation** — do not document cracker flags until Linux `aircrack-ng --help` is captured. Illustrative crack stdout (from operator experience / tutorials, not Captured help):

```
Reading packets, please wait...
Opening wpa_capture-01.cap
...
KEY FOUND! [ password123 ]
```

Parse `KEY FOUND` lines for credential events (authorized assessments only) when observed on a working Linux binary.

---

## aireplay-ng / airmon-ng stdout

- `airmon-ng start` → prints monitor interface name — capture for automation.
- `aireplay-ng -9` → injection working / failed — gate for replay workflows.
- `aireplay-ng -0` → packet counts sent — confirm deauth executed.

---

## wpaclean usage

Extract handshake-only caps before crack:

```bash
wpaclean clean.cap noisy-01.cap
aircrack-ng -b <BSSID> -w wordlist.txt clean.cap
```

---

## Related

- [nugget-mapping.md](nugget-mapping.md) — rows → `WIFI_ACCESS_POINT`
- `.cursor/skills/textfsm/SKILL.md` — TextFSM authoring
- [workflows.md](workflows.md) — when to produce CSV
