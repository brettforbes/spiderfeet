# NTC Templates — Canonical Sources

## Official documentation

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/networktocode/ntc-templates |
| Read the Docs home | https://ntc-templates.readthedocs.io |
| User overview | https://ntc-templates.readthedocs.io/en/latest/user/lib_overview/ |
| Use cases | https://ntc-templates.readthedocs.io/en/latest/user/lib_use_cases/ |
| Getting started | https://ntc-templates.readthedocs.io/en/latest/user/lib_getting_started/ |
| FAQ | https://ntc-templates.readthedocs.io/en/latest/user/faq/ |
| Install | https://ntc-templates.readthedocs.io/en/latest/admin/install/ |
| Upgrade | https://ntc-templates.readthedocs.io/en/latest/admin/upgrade/ |
| Extending | https://ntc-templates.readthedocs.io/en/latest/dev/extending/ |
| Contributing | https://ntc-templates.readthedocs.io/en/latest/dev/contributing/ |
| Dev environment | https://ntc-templates.readthedocs.io/en/latest/dev/dev_environment/ |
| Parser development | https://ntc-templates.readthedocs.io/en/latest/dev/dev_parser/ |
| `parse_output` API | https://ntc-templates.readthedocs.io/en/latest/dev/code_reference/parse/ |

## Install

```bash
pip install ntc-templates textfsm
```

Requires **textfsm** (CliTable). On Windows, ensure a working TextFSM build (see FAQ if `HAS_CLITABLE` fails).

## Articles

| Title | URL |
|-------|-----|
| PyNet — Netmiko and TextFSM | https://pynet.twb-tech.com/blog/netmiko-and-textfsm.html |
| CLI parsing strategies | https://www.networkershome.com/fundamentals/python-networking/cli-parsing-textfsm-ttp-genie/ |
| NTC parsing strategies (NTC blog) | https://networktocode.com/blog/parsing-strategies-ntc-templates/ |
| Contributing templates | https://theworldsgonemad.net/2025/add-ntc-template/ |
| Ansible Network Engine | https://josh-v.com/ansible-network-engine-ntc-templates/ |

## SpiderFeet notes

- NTC ships **network-device** templates (Cisco, Juniper, …). OSINT CLI tools (nmap text, netdiscover, naabu) need **project-local** templates under a custom `template_dir`.
- Use **`platform`** slugs like `spiderfeet_netdiscover`, `spiderfeet_naabu` in your index — not vendor names unless output matches NTC stock templates.
- Prefer **JSON/XML structured output** from CLI tools when available; use NTC/TextFSM only for text-only modes per `proj-06-spiderfeet-cli-app-exercising`.

## Environment

| Variable / path | Purpose |
|-----------------|--------|
| Default template dir | Packaged inside `ntc_templates` after pip install |
| `template_dir=` arg | Override to project templates (must contain `index`) |
| `NTC_TEMPLATES_DIR` | Optional env override (see package `_get_template_dir`) |
