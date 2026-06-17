# PIUS Sources

## Canonical upstream

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/praetorian-inc/pius |
| Install | `go install github.com/praetorian-inc/pius/cmd/pius@latest` |
| Plugin interface | `pkg/plugins/plugin.go` |
| Pipeline runner | `pkg/runner/` |
| Finding types | `Type`: `domain`, `cidr`, `cidr-handle` (internal) |

## Blog and announcements

| Title | URL |
|-------|-----|
| Mapping the Unknown: Introducing Pius | https://www.praetorian.com/blog/attack-surface-mapping-tool-pius/ |
| Attack Surface Management with Pius (LinkedIn) | https://www.linkedin.com/posts/praetorian_offensivesecurity-attacksurfacemanagement-activity-7438266584684457984-GYf_ |

## SpiderFeet project references

| Artifact | Path |
|----------|------|
| Skill prompt seed | `.seed/03I_Prompt_Making_for_Pius.md` |
| Zero to Hero | `.docs/docs-for-cli-tools/PIUS-Zero-to-Hero.md` |
| CLI options doc | `.docs/docs-for-cli-tools/PIUS-CLI-Options.md` |
| Nugget definitions | `.docs/analysis/nuggets.json` (`INTERNET_NAME`, `NETBLOCK_OWNER`) |
| Related CLI skills | `.cursor/skills/wafwoof/`, `.cursor/skills/cmseek/`, `.cursor/skills/nuclei/`, `.cursor/skills/nmap/`, `.cursor/skills/nerva/` |

## Comparison references (from upstream README)

| Tool | Pius advantage |
|------|----------------|
| subfinder | Pius adds RIR CIDR discovery + phased pipeline |
| amass | Pius adds confidence scoring + all 5 RIR handle resolution |

## License

Apache 2.0 — Praetorian Security, Inc.

## Security note

Authorized asset discovery only. Active plugins generate DNS traffic to targets.
