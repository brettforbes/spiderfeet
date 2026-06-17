# Nerva Sources

Canonical and supplementary material for this skill.

## Official repository and wiki

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/praetorian-inc/nerva |
| Releases (binaries) | https://github.com/praetorian-inc/nerva/releases |
| Documentation hub | https://github.com/praetorian-inc/nerva/wiki |
| CLI Reference | https://github.com/praetorian-inc/nerva/wiki/CLI-Reference |
| Protocol List (54 plugins) | https://github.com/praetorian-inc/nerva/wiki/Protocol-List |
| Integration Guide | https://github.com/praetorian-inc/nerva/wiki/Integration-Guide |
| Library Usage | https://github.com/praetorian-inc/nerva/wiki/Library-Usage |
| Plugin Development | https://github.com/praetorian-inc/nerva/wiki/Plugin-Development |
| SCTP Support | https://github.com/praetorian-inc/nerva/wiki/SCTP-Support |

## Blog posts

| Resource | URL | Notes |
|----------|-----|-------|
| Praetorian launch post | https://www.praetorian.com/blog/whats-running-on-that-port-introducing-nerva-for-service-fingerprinting/ | Pipeline positioning, 120+ checks |
| Medium builder post | https://medium.com/@praetorianguard/i-built-an-open-source-service-fingerprinter-heres-what-it-finds-0daae3ccc74a | Protocol depth examples |

## Related SpiderFeet skills

| Skill | Path | Role |
|-------|------|------|
| Netdiscover | `.cursor/skills/netdiscover/SKILL.md` | Upstream L2 host discovery |
| Nmap | `.cursor/skills/nmap/SKILL.md` | Port discovery |
| TextFSM | `.cursor/skills/textfsm/SKILL.md` | Not used for nerva (`--json` instead) |

## Operator documentation (this repo)

| Doc | Path |
|-----|------|
| Zero to Hero | `.docs/docs-for-cli-tools/Nerva-Zero-to-Hero.md` |
| CLI options | `.docs/docs-for-cli-tools/Nerva-CLI-Options.md` |

## Upstream port scanners (integration)

| Tool | URL |
|------|-----|
| Naabu | https://github.com/projectdiscovery/naabu |
| Masscan | https://github.com/robertdavidgraham/masscan |
| Nmap | https://nmap.org/ |

## Install

```bash
go install github.com/praetorian-inc/nerva/cmd/nerva@latest
```

Or download prebuilt binary from releases for Linux, macOS, Windows.

## Version notes

- Wiki documents **54 plugins**; blog references broader protocol coverage via multi-probe behavior.
- SCTP requires Linux scanner host.
- Always verify local `nerva -h` for flag compatibility.
