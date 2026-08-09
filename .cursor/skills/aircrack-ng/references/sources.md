# Aircrack-ng Sources

Canonical documentation for skill maintenance and operator learning.

## This host (2026-08-10)

| Resource | Path / note |
|----------|-------------|
| Windows suite extract | `.tools/aircrack-ng/aircrack-ng-1.7-win/` |
| Help captures | `.tmp_aircrack_help/*.txt` |
| Combined Captured help | `.docs/docs-for-cli-tools/Aircrack-Ng-CLI-Options.md` |
| **airmon-ng** | Not in Windows zip — Linux/WSL |
| **aircrack-ng** help | Proven limitation: `The system cannot execute the specified program` — re-capture on Linux |

## Official project

| Resource | URL |
|----------|-----|
| GitHub | https://github.com/aircrack-ng/aircrack-ng |
| Main site | https://www.aircrack-ng.org/ |
| Documentation index | https://www.aircrack-ng.org/doku.php |

## Suite tool pages

| Tool | URL |
|------|-----|
| airmon-ng | https://www.aircrack-ng.org/doku.php?id=airmon-ng |
| airodump-ng | https://www.aircrack-ng.org/doku.php?id=airodump-ng |
| aireplay-ng | https://www.aircrack-ng.org/doku.php?id=aireplay-ng |
| aircrack-ng | https://www.aircrack-ng.org/doku.php?id=aircrack-ng |
| airbase-ng | https://www.aircrack-ng.org/doku.php?id=airbase-ng |
| airdecap-ng | https://www.aircrack-ng.org/doku.php?id=airdecap-ng |
| airdecloak-ng | https://www.aircrack-ng.org/doku.php?id=airdecloak-ng |
| airdrop-ng | https://www.aircrack-ng.org/doku.php?id=airdrop-ng |
| airgraph-ng | https://www.aircrack-ng.org/doku.php?id=airgraph-ng |
| airolib-ng | https://www.aircrack-ng.org/doku.php?id=airolib-ng |
| besside-ng | https://www.aircrack-ng.org/doku.php?id=besside-ng |
| easside-ng | https://www.aircrack-ng.org/doku.php?id=easside-ng |
| wesside-ng | https://www.aircrack-ng.org/doku.php?id=wesside-ng |

## Tutorials

| Topic | URL |
|-------|-----|
| WPA capture | https://www.aircrack-ng.org/doku.php?id=wpa_capture |
| Crack WPA/WPA2 | https://www.aircrack-ng.org/doku.php?id=cracking_wpa |
| ARP injection capture | https://www.aircrack-ng.org/doku.php?id=arp_inject_capture |
| ARP amplification | https://www.aircrack-ng.org/doku.php?id=arp_amplification |
| Simple WEP crack | https://www.aircrack-ng.org/doku.php?id=simple_wep_crack |
| WEP flowchart | https://www.aircrack-ng.org/doku.php?id=flowchart |
| WEP no clients | https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_with_no_clients |
| WEP via client | https://www.aircrack-ng.org/doku.php?id=how_to_crack_wep_via_a_wireless_client |
| Shared key auth | https://www.aircrack-ng.org/doku.php?id=shared_key |
| WDS WEP | https://www.aircrack-ng.org/doku.php?id=wds |
| IVs not increasing | https://www.aircrack-ng.org/doku.php?id=i_am_injecting_but_the_ivs_don_t_increase |

## Additional references

| Resource | URL |
|----------|-----|
| Legacy FAQ / docs | https://www.tuto-fr.com/tutoriaux/crack-wep/FAQ/en-aircrack-documentation.php |
| Secure Ideas intro | https://www.secureideas.com/blog/2018/09/introduction-to-wireless-security-with-aircrack-ng.html |
| BHIS airodump-ng | https://www.blackhillsinfosec.com/hunt-for-weak-spots-in-your-wireless-network-with-airodump-ng/ |
| SecureWithSiva deep dive | https://securewithsiva.in/post/08-aircrack-ng/ |

## SpiderFeet project files

| Resource | Path |
|----------|------|
| Skill entry | `.cursor/skills/aircrack-ng/SKILL.md` |
| TextFSM skill | `.cursor/skills/textfsm/SKILL.md` |
| WIFI nugget | `.docs/analysis/nuggets.json` (`WIFI_ACCESS_POINT`) |
| Zero to Hero | `.docs/docs-for-cli-tools/Aircrack-Ng-Zero-to-Hero.md` |
| CLI options | `.docs/docs-for-cli-tools/Aircrack-Ng-CLI-Options.md` |

## Hardware notes

Compatible adapter lists change frequently. Verify monitor mode and injection with `airmon-ng start` (Linux) and `aireplay-ng --test` / `-9` before relying on third-party chipset charts.
