# Subfinder Source Material

## Official

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/projectdiscovery/subfinder |
| Go examples | https://github.com/projectdiscovery/subfinder/tree/dev/v2/examples |
| Overview | https://docs.projectdiscovery.io/opensource/subfinder/overview |
| Install | https://docs.projectdiscovery.io/opensource/subfinder/install |
| Running | https://docs.projectdiscovery.io/opensource/subfinder/running |
| Usage / flags | https://docs.projectdiscovery.io/opensource/subfinder/usage |
| ProjectDiscovery blog | https://projectdiscovery.io/blog |

## Install methods

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Releases: https://github.com/projectdiscovery/subfinder/releases

Docker: `projectdiscovery/subfinder:latest`

## Articles and tutorials

| Title | URL |
|-------|-----|
| SecurityTrails — Subfinder | https://securitytrails.com/blog/subfinder |
| Recon with me (Subfinder) | https://dhiyaneshgeek.github.io/bug/bounty/2020/02/06/recon-with-me/ |
| Subfinder + SecurityTrails (2024) | https://dhiyaneshgeek.github.io/research,bug/bounty/2024/01/03/subfinder-securitytrails/ |
| Hacklido enumeration guide | https://hacklido.com/blog/390-subdomain-enumeration-using-subfinder |
| GeeksforGeeks overview | https://www.geeksforgeeks.org/linux-unix/subfinder-a-subdomain-discovery-tool-in-kali-linux/ |
| freeCodeCamp enumeration | https://www.freecodecamp.org/news/using-subfinder-for-subdomain-enumeration/ |
| YouTube search | https://www.youtube.com/results?search_query=projectdiscovery+subfinder |

Search InfosecWriteups and SystemWeakness for additional walkthroughs.

## Related SpiderFeet repo artifacts

| Path | Role |
|------|------|
| `.cursor/skills/subfinder/SKILL.md` | Agent skill entry |
| `.docs/docs-for-cli-tools/SubFinder-Zero-to-Hero.md` | Operator guide |
| `.docs/docs-for-cli-tools/SubFinder-CLI-Options.md` | CLI reference |
| `modules/sfp_sublist3r.py` | Legacy API module pattern for subdomain nuggets |
| `.seed/03ZB_Prompt_Making_for_Subfinder.md` | Skill authoring prompt |

## Downstream ProjectDiscovery tools

| Tool | Chain role |
|------|------------|
| dnsx | Resolve and filter candidates |
| httpx | Probe HTTP services |
| naabu | Port scan live hosts |
| nuclei | Vulnerability templates |

Skills: `.cursor/skills/dnsx/`, `naabu/`, `nuclei/`.
