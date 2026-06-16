# CMSeeK Sources

## Canonical upstream

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/Tuhinshubhra/CMSeeK |
| Entry point | `cmseek.py` |
| Core detection | `cmseekdb/core.py` |
| Result logging | `cmseekdb/basic.py` (`update_log`, `handle_quit`) |

## Blog and tutorial references

| Title | URL |
|-------|-----|
| CMSeeK — Detect CMS and Exploitation Suit (Kali Linux) | https://www.kalilinux.in/cmseek-detect-cms-and-exploitation-suit/ |
| CMSeek – CMS Detection and Information Gathering | https://latesthackingnews.com/2018/09/10/cmseek-cms-detection-and-information-gathering/ |
| CMSeeK - CMS Detection and Exploitation Tool (GeeksforGeeks) | https://www.geeksforgeeks.org/linux-unix/cmseek-cms-detection-and-exploitation-tool/ |

## SpiderFeet project references

| Artifact | Path |
|----------|------|
| Module source | `modules/sfp_tool_cmseek.py` |
| Install runbook | `.docs/analysis/cli_tool_install_runbook.md` |
| Module analysis | `.docs/analysis/conversion_to_types/modules/sfp_tool_cmseek.md` |
| OSINT service doc | `.docs/osint-services/modules/sfp_tool_cmseek.md` |
| Nugget producers | `.docs/analysis/conversion_to_types/nugget_type_producers.md` (`WEBSERVER_TECHNOLOGY`) |
| Skill prompt seed | `.seed/03G_Prompt_Making_for_CMSeeK.md` |
| Zero to Hero | `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md` |
| CLI options doc | `.docs/docs-for-cli-tools/CMSeeK-CLI-Options.md` |

## Related SpiderFeet tools

| Tool | Relationship |
|------|----------------|
| WAFWOOF (`sfp_tool_wafw00f`) | Run before CMSeeK when WAF may block fingerprinting |
| WhatWeb / BuiltWith modules | Overlapping web technology discovery |
| Nuclei | Version-aware templates after CMS identification |

## Install notes (SpiderFeet)

- **Linux / WSL:** clone repo, run with `python3 cmseek.py`
- **Windows native:** unreliable; use WSL2 per `cli_tool_install_runbook.md`
- **SpiderFeet opts:** `cmseekpath` must point at install root containing `cmseek.py`
