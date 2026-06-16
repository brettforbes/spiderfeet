# Nuclei Sources

Canonical documentation and learning material for skill maintenance.

## ProjectDiscovery — Nuclei engine

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/projectdiscovery/nuclei |
| Overview | https://docs.projectdiscovery.io/opensource/nuclei/overview |
| Installation | https://docs.projectdiscovery.io/opensource/nuclei/install |
| Running Nuclei | https://docs.projectdiscovery.io/opensource/nuclei/running |
| CI/CD | https://docs.projectdiscovery.io/opensource/nuclei/ci-cd |
| Input formats | https://docs.projectdiscovery.io/opensource/nuclei/input-formats |
| Authenticated scans | https://docs.projectdiscovery.io/opensource/nuclei/authenticated-scans |
| Mass scanning | https://docs.projectdiscovery.io/opensource/nuclei/mass-scanning-cli |
| Nuclei SDK | https://docs.projectdiscovery.io/opensource/nuclei/nuclei-sdk |
| Community templates repo | https://github.com/projectdiscovery/nuclei-templates |

## ProjectDiscovery — Template authoring

| Resource | URL |
|----------|-----|
| Introduction | https://docs.projectdiscovery.io/templates/introduction |
| Structure | https://docs.projectdiscovery.io/templates/structure |
| FAQ | https://docs.projectdiscovery.io/templates/faq |
| HTTP basic | https://docs.projectdiscovery.io/templates/protocols/http/basic-http |
| Raw HTTP | https://docs.projectdiscovery.io/templates/protocols/http/raw-http |
| Fuzzing overview | https://docs.projectdiscovery.io/templates/protocols/http/fuzzing-overview |
| Headless | https://docs.projectdiscovery.io/templates/protocols/headless |
| Network | https://docs.projectdiscovery.io/templates/protocols/network |
| DNS | https://docs.projectdiscovery.io/templates/protocols/dns |
| Matchers | https://docs.projectdiscovery.io/templates/reference/matchers |
| Extractors | https://docs.projectdiscovery.io/templates/reference/extractors |
| Workflows overview | https://docs.projectdiscovery.io/templates/workflows/overview |
| Workflow examples | https://docs.projectdiscovery.io/templates/workflows/examples |

## Blogs and guides

| Resource | URL |
|----------|-----|
| Bishop Fox — Nuclei vulnerability scanning | https://bishopfox.com/blog/nuclei-vulnerability-scan |
| Bugcrowd — Beginner's guide | https://www.bugcrowd.com/blog/the-ultimate-beginners-guide-to-nuclei/ |
| Orca — Cloud templates | https://orca.security/resources/blog/using-nuclei-templates-for-vulnerability-scanning/ |
| PD — Custom templates | https://projectdiscovery.io/blog/if-youre-not-writing-custom-nuclei-templates-youre-missing-out |
| PD — Universal language of vulnerabilities | https://projectdiscovery.io/blog/the-power-of-nuclei-templates-a-universal-language-of-vulnerabilities |

## SpiderFeet project files

| Resource | Path |
|----------|------|
| Module source | `modules/sfp_tool_nuclei.py` |
| Conversion example | `.docs/analysis/conversion_to_types/examples/sfp_tool_nuclei.md` |
| Zero to Hero (operator) | `.docs/docs-for-cli-tools/Nuclei-Zero-to-Hero.md` |
| CLI options (operator) | `.docs/docs-for-cli-tools/Nuclei-CLI-Options.md` |
| Skill entry | `.cursor/skills/nuclei/SKILL.md` |

## Template installation paths

SpiderFeet resolves templates via `spiderfeet.tools.cli_paths.resolve_nuclei_templates()` — typically `.tools/nuclei-templates` in the repo or operator-configured path.
