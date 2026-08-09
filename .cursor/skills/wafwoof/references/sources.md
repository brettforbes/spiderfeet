# WAFWOOF Sources

## Canonical upstream

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/EnableSecurity/wafw00f |
| Getting Started wiki | https://github.com/EnableSecurity/wafw00f/wiki/Getting-Started |
| Usage / arguments | https://github.com/EnableSecurity/wafw00f/wiki/Usage |
| JSON builder | `wafw00f/main.py` → `buildResultRecord()` |

**Note:** Published package and binary name is `wafw00f` (three zeros). Skill directory is `wafwoof`.

## Blog and tutorial references

| Title | URL |
|-------|-----|
| WAFW00F — Web Application Firewall Fingerprinting | https://cbhsecurity.medium.com/wafw00f-web-application-firewall-fingerprinting-4e7853633bff |
| Identification of WAF using WAFW00F (GeeksforGeeks) | https://www.geeksforgeeks.org/linux-unix/identification-of-web-application-firewall-using-wafw00f-in-kali-linux/ |
| Detecting Web Application Firewalls (pentestlab) | https://pentestlab.blog/2013/01/13/detecting-web-application-firewalls/ |
| Fingerprinting WAF using Wafw00f (stratosally) | https://www.stratosally.com/offensive-security/web-application-4890 |

## Man pages

| Platform | URL |
|----------|-----|
| Debian manpage | https://manpages.debian.org/wafw00f |

## SpiderFeet project references

| Artifact | Path |
|----------|------|
| Module source | `modules/sfp_tool_wafw00f.py` |
| Install runbook | `.docs/analysis/cli_tool_install_runbook.md` (`pip install wafw00f`) |
| OSINT service doc | `.docs/osint-services/modules/sfp_tool_wafw00f.md` |
| Manifest migration candidate | `.seed/planning/issues/cli-799-migrate-three.md` |
| Skill prompt seed | `.seed/03H_Prompt_Making_for_WAFWOOF.md` |
| Zero to Hero | `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md` |
| CLI options doc | `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md` |
| Captured help (v2.4.2) | `.venv/Scripts/wafw00f.exe --help` (2026-08-10) |

## Related tools

| Tool | Relationship |
|------|----------------|
| CMSeeK | Run after WAF detect; may need UA rotation |
| Nuclei | Rate/template selection based on WAF |
| PIUS | Supplies `INTERNET_NAME` candidates for WAF sweep |
