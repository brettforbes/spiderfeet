# Naabu — Canonical Sources

## Official documentation

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/projectdiscovery/naabu |
| Overview | https://docs.projectdiscovery.io/opensource/naabu/overview |
| Install | https://docs.projectdiscovery.io/opensource/naabu/install |
| Usage | https://docs.projectdiscovery.io/opensource/naabu/usage |
| Running | https://docs.projectdiscovery.io/opensource/naabu/running |

## Install notes

| Platform | Prerequisite |
|----------|--------------|
| Linux | `libpcap-dev` — `sudo apt install -y libpcap-dev` |
| macOS | `brew install libpcap` |
| Windows | [Npcap](https://npcap.com/) |

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
| Medium — bug hunters | https://medium.com/@loyalonlytoday/naabu-powerful-portscanning-tool-for-bug-hunters-758860a6526b |
| FreshPorts | https://www.freshports.org/security/naabu/ |

## SpiderFeet integration

- **Always** capture **`naabu ... -json`** (JSON Lines) for formal examination.
- Default scan assumes VPS-grade rate; tune `-rate` on local workstations.
- **Root/admin** recommended for SYN scans (`-s s`); non-root falls back to CONNECT (`-s c` default).
- Chain: **dnsx/subfinder → naabu → httpx / nerva / nmap / julius**.

## Metrics endpoint

Live scan stats: `http://localhost:63636/metrics` (change with `-metrics-port`).
