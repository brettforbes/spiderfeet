# Naabu — Canonical Sources

## Official documentation

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/projectdiscovery/naabu |
| Overview | https://docs.projectdiscovery.io/opensource/naabu/overview |
| Install | https://docs.projectdiscovery.io/opensource/naabu/install |
| Usage | https://docs.projectdiscovery.io/opensource/naabu/usage |
| Running | https://docs.projectdiscovery.io/opensource/naabu/running |

## Local capture (authoritative for this skill)

| Item | Path / value |
|------|----------------|
| Windows binary | `C:\projects\spiderfeet\.tools\naabu\naabu.exe` |
| Version | **2.6.1** |
| Capture date | **2026-08-10** |
| Help dumps | `.tmp_naabu_help/help_h.txt`, `help_long.txt`, `version.txt` |

Online Usage pages can lag the binary (missing SERVICES-DISCOVERY, CLOUD, smart-scan, etc.). **Prefer live `-h`.**

## Install notes

| Platform | Prerequisite |
|----------|--------------|
| Linux | `libpcap-dev` — `sudo apt install -y libpcap-dev` |
| macOS | `brew install libpcap` |
| Windows | [Npcap](https://npcap.com/) for SYN / raw; CONNECT works without elevation |

```bash
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
naabu -version
```

Releases: https://github.com/projectdiscovery/naabu/releases

## Articles and guides

| Title | URL |
|-------|-----|
| Improving port scans against API servers | https://danaepp.com/improving-port-scans-against-api-servers |
| Naabu details (RootSec) | https://www.rootsec.in/tools/port-scanning/network-scanners/naabu |
| Naabu cheat sheet | https://highon.coffee/blog/naabu-cheat-sheet/ |
| YesWeHack recon port scanning | https://www.yeswehack.com/learn-bug-bounty/recon-port-scanning-attack-vectors |
| Port scanning fundamentals | https://www.hackingloops.com/port-scanning-in-cybersecurity/ |
| Medium — bug hunters | https://medium.com/@loyalonlytoday/naabu-powerful-portscanning-tool-for-bug-hunters-758860a6526b |
| FreshPorts | https://www.freshports.org/security/naabu/ |
| Brief note | https://mrshan.medium.com/naabu-port-scanner-why-you-should-use-it-947d8ca025df |

## SpiderFeet integration

- **Always** capture **`naabu ... -json`** (JSON Lines) for formal examination.
- Default scan assumes VPS-grade rate; tune `-rate` on local workstations.
- **This Windows binary** defaults to CONNECT (`-s c`); SYN needs privileges (`naabu -hc` → `Privileged/NET_RAW`).
- Chain: **dnsx/subfinder → naabu → httpx / nerva / nmap / julius**.

## Metrics endpoint

Live scan stats: `http://localhost:63636/` (change with `-metrics-port`; help default `63636`).
