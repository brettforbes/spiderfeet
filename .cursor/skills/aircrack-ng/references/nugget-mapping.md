# Aircrack-ng → SpiderFeet Nugget Mapping

Wireless discovery and assessment outputs mapped to SpiderFeet nugget types. No `sfp_tool_aircrack` module exists in core SpiderFeet today — this document defines the **target contract** for a future CLI integration or TextFSM parser.

## Primary nugget types

| Nugget ID | Type | Source |
|-----------|------|--------|
| `WIFI_ACCESS_POINT` | ENTITY | airodump AP row |
| `MAC_ADDRESS` | ENTITY | BSSID, station MAC |
| `HUMAN_NAME` / descriptor | DESCRIPTOR | ESSID (network name) |

Confirm additional types in `.docs/analysis/nuggets.json` when extending the catalogue.

---

## AP row → `WIFI_ACCESS_POINT`

**Trigger:** Each unique BSSID in airodump AP table.

**Node data (suggested):**

```json
{
  "bssid": "AA:BB:CC:DD:EE:FF",
  "essid": "CorpWiFi",
  "channel": "6",
  "privacy": "WPA2",
  "cipher": "CCMP",
  "authentication": "PSK",
  "power_dbm": "-42",
  "beacons": "120",
  "first_seen": "...",
  "last_seen": "..."
}
```

**Event text format (SpiderFeet style):**

```
ESSID: CorpWiFi
BSSID: AA:BB:CC:DD:EE:FF
Channel: 6
Encryption: WPA2 CCMP PSK
Signal: -42 dBm
```

**Edges:**

- Scan seed (location, `IP_ADDRESS`, or investigation root) → `discovered` → `WIFI_ACCESS_POINT`
- `WIFI_ACCESS_POINT` → `has_bssid` → `MAC_ADDRESS` (BSSID)

---

## Hidden SSID

When `ESSID` is `<length: 0>` or empty:

- Emit `WIFI_ACCESS_POINT` with `essid: null` or `hidden: true`
- Add probed ESSIDs from station table as `HUMAN_NAME` descriptors linked to station MAC

---

## Station row → client entities

| Parsed field | Nugget | Relation |
|--------------|--------|----------|
| Station MAC | `MAC_ADDRESS` | `client_of` → AP `WIFI_ACCESS_POINT` |
| Probed ESSIDs | Descriptor / `HUMAN_NAME` | `probed` → station MAC |
| Associated BSSID | Link only | Resolve AP node |

---

## Handshake / crack outcomes (authorized pentest only)

| Outcome | Suggested event | Notes |
|---------|-----------------|-------|
| WPA handshake captured | `DESCRIPTOR` on AP | `WPA handshake captured` — not a crack |
| `KEY FOUND` from aircrack-ng | `PASSWORD` / `CREDENTIAL` (if in catalogue) | Scope-gated; never emit for unauthorized scans |
| WEP key recovered | `DESCRIPTOR` | Legacy; document encryption broken |

Default **OSINT discovery** integrations should **not** emit credentials — only `WIFI_ACCESS_POINT` + topology.

---

## airgraph-ng output

PNG/graph files are artifacts — attach as scan metadata or `RAW_FILE` descriptor if module supports file events. Graph edges mirror AP↔client associations.

---

## Decision flow

```
airodump CSV parsed
    │
    ├─ AP row (unique BSSID)
    │       └─ WIFI_ACCESS_POINT + MAC_ADDRESS (BSSID)
    │
    ├─ Station row (associated)
    │       └─ MAC_ADDRESS + edge to AP
    │
    ├─ Station probed ESSIDs
    │       └─ HUMAN_NAME/descriptor → station
    │
    └─ (optional pentest) handshake/crack stdout
            └─ DESCRIPTOR or CREDENTIAL per policy
```

---

## Example mapping function

```python
def ap_row_to_nodes_edges(row: dict, seed_id: str) -> tuple[list, list]:
    ap_id = f"wifi:{row['BSSID']}"
    mac_id = f"mac:{row['BSSID']}"
    text = (
        f"ESSID: {row['ESSID']}\n"
        f"BSSID: {row['BSSID']}\n"
        f"Channel: {row['CHANNEL']}\n"
        f"Encryption: {row['PRIVACY']} {row['CIPHER']} {row['AUTH']}\n"
        f"Signal: {row['POWER']} dBm"
    )
    nodes = [
        {"id": ap_id, "type": "WIFI_ACCESS_POINT", "data": text},
        {"id": mac_id, "type": "MAC_ADDRESS", "data": row["BSSID"]},
    ]
    edges = [
        {"source": seed_id, "target": ap_id, "relation": "discovered"},
        {"source": ap_id, "target": mac_id, "relation": "has_bssid"},
    ]
    return nodes, edges
```

---

## Module integration checklist (future `sfp_tool_aircrack`)

1. Resolve `airodump-ng` / `airmon-ng` on PATH
2. Guard: compatible adapter present; fail with clear error if monitor mode fails
3. Run Workflow 1 (passive survey) by default — no `aireplay-ng` in OSINT mode
4. Parse latest CSV via TextFSM
5. Emit `WIFI_ACCESS_POINT` per AP; dedupe by BSSID per scan
6. Optional module flag: `injection_allowed` for pentest handshake workflow

---

## Related

- [output-and-parsing.md](output-and-parsing.md)
- `.docs/analysis/nuggets.json` — `WIFI_ACCESS_POINT`
- `.cursor/skills/textfsm/references/nugget-conversion.md`
