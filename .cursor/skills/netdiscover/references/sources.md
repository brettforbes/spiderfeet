# Netdiscover Sources

Canonical and supplementary material for this skill.

## Official

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/netdiscover-scanner/netdiscover |
| Man page (Ubuntu) | https://manpages.ubuntu.com/manpages/bionic/man8/netdiscover.8.html |
| Legacy SourceForge | https://sourceforge.net/projects/netdiscover/ |

## Guides and articles

| Resource | URL | Notes |
|----------|-----|-------|
| InfosecOne command guide | https://infosecone.com/blog/netdiscover-command-network-discovery-tool/ | `-P` samples, per-flag examples |
| Geek Institute ARP tool overview | https://blog.geekinstitute.org/2025/05/netdiscover-arp-based-network-discovery-tool.html | Pentest-oriented workflow |
| ExamCollection visibility guide | https://www.examcollection.com/blog/unlocking-network-visibility-how-to-discover-hosts-efficiently-with-netdiscover/ | Discovery efficiency |
| Spread Security: Nmap + Netdiscover | https://spreadsecurity.github.io/2016/09/25/network-discovery-with-nmap-and-netdiscover.html | Layered discovery, passive vs active |

## Related SpiderFeet skills

| Skill | Path |
|-------|------|
| TextFSM parsing | `.cursor/skills/textfsm/SKILL.md` |
| Nmap | `.cursor/skills/nmap/SKILL.md` |
| Nerva fingerprinting | `.cursor/skills/nerva/SKILL.md` |

## Operator documentation (this repo)

| Doc | Path |
|-----|------|
| Zero to Hero | `.docs/docs-for-cli-tools/NetDiscover-Zero-to-Hero.md` |
| CLI options | `.docs/docs-for-cli-tools/NetDiscover-CLI-Options.md` |

## Libraries

Netdiscover is built on **libpcap** and **libnet**. Packet capture behavior follows standard BPF filtering when `-F` is used.

## Version notes

- Package versions vary (`0.3beta7` on older distros; newer git builds add `-N`, `-m`, `-F`).
- Always run `netdiscover -h` on the target host to confirm available flags before scripting.
