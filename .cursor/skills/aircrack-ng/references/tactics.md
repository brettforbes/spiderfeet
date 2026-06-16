# Aircrack-ng Tactics

Adaptive wireless sequences when RF conditions, defenses, or hardware limit discovery and capture.

## Principles

1. **Passive before active** — Maximize airodump survey before any `aireplay-ng`.
2. **Fix channel early** — Channel hopping misses short beacons; lock `-c` once BSSID known.
3. **BSSID over ESSID** — Duplicate SSIDs are common; always key on BSSID.
4. **Adapter matters more than wordlists** — Injection failures block WEP/WPA acceleration.
5. **Authorized disruption only** — Deauth is a denial-of-service; scope explicitly.

---

## Tactic 1: Noisy RF environment

**Symptoms:** APs flicker, power readings unstable, incomplete client list.

| Step | Action |
|------|--------|
| 1 | Move closer to target airspace (authorized physical access) |
| 2 | Reduce hop rate: airodump `-d 500` or fixed channel |
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
| 3 | Authorized: single targeted `aireplay-ng -0 1` (minimal disruption) |
| 4 | Retry at shift change / high client mobility windows |
| 5 | Consider PMKID capture tools if engagement allows (outside classic aircrack) |

---

## Tactic 4: WEP IV stagnation

**Symptoms:** `# IV` not increasing during ARP replay.

| Step | Action |
|------|--------|
| 1 | Verify injection: `aireplay-ng -9` |
| 2 | Re-fake-auth: `aireplay-ng -1 0` |
| 3 | Try different client MAC `-h` |
| 4 | Switch attack: chopchop `-4`, fragmentation `-5` |
| 5 | Read [IVs don't increase](https://www.aircrack-ng.org/doku.php?id=i_am_injecting_but_the_ivs_don_t_increase) |

---

## Tactic 5: Clientless WEP AP

**Reference:** [Crack WEP with no clients](https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_with_no_clients)

| Step | Action |
|------|--------|
| 1 | Fake authentication |
| 2 | Fragmentation or chopchop to obtain PRGA |
| 3 | `packetforge-ng` + ARP replay |
| 4 | `aircrack-ng` when IV threshold met |

---

## Tactic 6: WPA crack throughput

**Symptoms:** Dictionary crack too slow.

| Step | Action |
|------|--------|
| 1 | `wpaclean` cap |
| 2 | `airolib-ng --batch` for target ESSID + wordlist |
| 3 | `aircrack-ng -r db` |
| 4 | Rule-based wordlist mangling before import |
| 5 | GPU tools (hashcat) if policy allows — export hccapx |

---

## Tactic 7: OSINT-only footprint

**Goal:** Maximum AP/client intelligence without injection.

| Step | Action |
|------|--------|
| 1 | Workflow 1 passive survey |
| 2 | Parse CSV → `WIFI_ACCESS_POINT` |
| 3 | `airgraph-ng` for association graph |
| 4 | Correlate BSSIDs with OUI/manufacturer (`--manufacturer`) |
| 5 | Stop — no aireplay/aircrack |

---

## Tactic 8: Driver / monitor mode flakiness

**Symptoms:** `wlan0mon` disappears, channel `-1`.

| Step | Action |
|------|--------|
| 1 | `airmon-ng check kill` and restart monitor |
| 2 | `--ignore-negative-one` |
| 3 | USB power saving off |
| 4 | Different chipset / `apt install` driver firmware |
| 5 | Kali maintained kernel + known-good Alfa adapter |

---

## Response matrix

| Observation | Next action |
|-------------|-------------|
| No APs at all | Check region, antenna, monitor mode, `iw reg get` |
| OPN (open) APs | Map as high-risk descriptor; no crack needed for presence |
| WPA3 only | Classic WPA handshake crack may not apply |
| Many clients, no handshake | Minimal deauth or wait for roaming |
| Duplicate ESSIDs | Report each BSSID separately |
| Injection test fails | Do not use replay tactics; passive only |

---

## Anti-patterns

- Deauth flooding entire channel
- Cracking or capturing without written authorization
- Assuming laptop built-in WiFi supports injection
- Ignoring teardown (`airmon-ng stop`) leaving NIC in monitor mode
- Emitting recovered passwords into OSINT graph by default

---

## Related

- [workflows.md](workflows.md)
- [cli-options-by-module.md](cli-options-by-module.md)
- [nugget-mapping.md](nugget-mapping.md)
