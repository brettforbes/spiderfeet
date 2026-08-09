# Aircrack-ng Tactics

Adaptive wireless sequences when RF conditions, defenses, or hardware limit discovery and capture.

## Principles

1. **Passive before active** — Maximize airodump survey before any `aireplay-ng`.
2. **Fix channel early** — Channel hopping misses short beacons; lock `--channel` once BSSID known.
3. **BSSID over ESSID** — Duplicate SSIDs are common; always key on BSSID.
4. **Adapter matters more than wordlists** — Injection failures block WEP/WPA acceleration.
5. **Authorized disruption only** — Deauth is a denial-of-service; scope explicitly.
6. **Runtime honesty** — On Windows: no `airmon-ng`; `aircrack-ng` help may be unusable — plan Linux/WSL for monitor + crack.

---

## Tactic 1: Noisy RF environment

**Symptoms:** APs flicker, power readings unstable, incomplete client list.

| Step | Action |
|------|--------|
| 1 | Move closer to target airspace (authorized physical access) |
| 2 | Reduce hop rate: airodump `-f 500` or fixed `--channel` |
| 3 | External directional antenna if legal and in scope |
| 4 | Longer passive window (10–30 min) |
| 5 | Merge multiple CSV snapshots; dedupe BSSIDs |

---

## Tactic 2: Hidden SSID discovery

**Symptoms:** `ESSID` length 0 in AP row.

| Step | Action |
|------|--------|
| 1 | Passive airodump; read station **Probed ESSIDs** |
| 2 | Correlate probe requests with station MAC → AP BSSID |
| 3 | Authorized: wait for client association revealing ESSID |
| 4 | Map as `hidden: true` AP until ESSID confirmed |

---

## Tactic 3: WPA handshake won't appear

**Symptoms:** No `WPA handshake:` in airodump after long wait.

| Step | Action |
|------|--------|
| 1 | Confirm client associated (`Station MAC` → target BSSID) |
| 2 | `wpaclean` on cap — handshake may exist but buried |
| 3 | Authorized: single targeted `aireplay-ng --deauth 1` (minimal disruption) |
| 4 | Retry at shift change / high client mobility windows |
| 5 | Consider PMKID capture tools if engagement allows (outside classic aircrack) |

---

## Tactic 4: WEP IV stagnation

**Symptoms:** `# IV` / data count not increasing during ARP replay.

| Step | Action |
|------|--------|
| 1 | `aireplay-ng --test` / `-9` — confirm injection |
| 2 | Fake auth (`--fakeauth`) then retry `--arpreplay` |
| 3 | See [IVs don't increase](https://www.aircrack-ng.org/doku.php?id=i_am_injecting_but_the_ivs_don_t_increase) |
| 4 | Try `--chopchop` / `--fragment` + `packetforge-ng` path |
| 5 | Clientless: `--caffe-latte` / `--cfrag` in lab only |

---

## Tactic 5: Protected / filtered airspace

**Symptoms:** Sparse CSV, few clients, short dwell.

| Step | Action |
|------|--------|
| 1 | Longer passive survey; avoid deauth |
| 2 | Record manufacturer/WPS columns (`--manufacturer`, `--wps`) for OSINT value |
| 3 | Treat sparse export as valid **clean_miss / sparse** fixture — do not invent APs |
| 4 | Escalate only with expanded authorization |

---

## Tactic 6: Windows host / missing monitor stack

**Symptoms:** Suite binaries present; no `airmon-ng`; cracker won't run.

| Step | Action |
|------|--------|
| 1 | Use Captured help for offline flag documentation |
| 2 | Move RF work to Linux/WSL with supported USB adapter |
| 3 | Re-capture `aircrack-ng --help` on Linux before documenting cracker flags |
| 4 | Keep SpiderFeet OSINT path as airodump CSV parse when captures exist |

---

## Tactic 7: Maximize returned data (orchestrated)

```
airmon-ng (Linux) → airodump survey (csv+pcap)
    → focus BSSID+channel
        → passive handshake wait
            → minimal authorized deauth if needed
                → wpaclean
                    → airolib-ng batch (optional)
                        → Linux aircrack-ng (help-gated flags)
                            → airdecap-ng → Wireshark
```

Branch by encryption (`Privacy` column): OPN (map only) / WEP (IV path) / WPA* (handshake path).
