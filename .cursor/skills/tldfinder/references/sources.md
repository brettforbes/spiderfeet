# tldfinder Sources

## Official docs and repository

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/projectdiscovery/tldfinder |
| README | https://github.com/projectdiscovery/tldfinder/blob/main/README.md |
| Releases | https://github.com/projectdiscovery/tldfinder/releases |
| Go package | https://pkg.go.dev/github.com/projectdiscovery/tldfinder |

## Research and announcements

| Title | URL |
|-------|-----|
| Enumerating private TLDs (Google Threat Intelligence) | https://cloud.google.com/blog/topics/threat-intelligence/enumerating-private-tlds |

## Supplementary guides

| Title | URL |
|-------|-----|
| tldfinder and Netlas | https://netlas.io/blog/tldfinder_and_netlas/ |
| Passive recon guide (HackMag) | https://hackmag.com/coding/passive-recon-guide |

## Install methods

```bash
go install github.com/projectdiscovery/tldfinder/cmd/tldfinder@latest
```

Pre-built releases: https://github.com/projectdiscovery/tldfinder/releases

This workspace binary (evidence **2026-08-10**):

- `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe` — **v0.0.2**
- Help captures: `.tmp_tldfinder_help/help_long.txt`, `help_h.txt`, `version.txt`

## Related SpiderFeet repo artifacts

| Path | Role |
|------|------|
| `.cursor/skills/tldfinder/SKILL.md` | Agent skill entry |
| `.docs/docs-for-cli-tools/tldfinder-Zero-to-Hero.md` | Operator guide |
| `.docs/docs-for-cli-tools/tldfinder-CLI-Options.md` | CLI reference |
| `.seed/03S_Prompt_Making_for_tldfinder.md` | Skill authoring prompt |

## Downstream ProjectDiscovery tools

| Tool | Chain role |
|------|------------|
| dnsx | Resolve and filter candidates |
| httpx | Probe HTTP services |
| naabu | Port scan live hosts |
| subfinder | Adjacent passive subdomain enumeration (public zones) |

Skills: `.cursor/skills/dnsx/`, `httpx/`, `naabu/`, `subfinder/`.
