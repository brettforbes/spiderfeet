# NTLMRecon Sources

## Official (canonical — SpiderFeet)

| Resource | URL |
|----------|-----|
| Repository | https://github.com/praetorian-inc/NTLMRecon |
| README | https://github.com/praetorian-inc/NTLMRecon/blob/main/README.md |
| Releases | https://github.com/praetorian-inc/NTLMRecon/releases |
| Blog — NTLM endpoint discovery | https://www.praetorian.com/blog/automating-the-discovery-of-ntlm-authentication-endpoints/ |
| CLI entrypoint | https://github.com/praetorian-inc/NTLMRecon/blob/main/cmd/NTLMRecon/NTLMRecon.go |
| JSON structs | https://github.com/praetorian-inc/NTLMRecon/blob/main/pkg/structs/structs.go |
| Embedded paths | https://github.com/praetorian-inc/NTLMRecon/blob/main/pkg/paths/paths.txt |

## Ecosystem / legacy (different tool)

| Resource | URL |
|----------|-----|
| Original Python tool (pwnfoo) | https://github.com/pwnfoo/NTLMRecon |
| OffSec KB (Python CLI) | https://kb.offsec.nl/tools/other/ntlmrecon/ |
| Practitioner overview | https://pentesttools.net/ntlmrecon-enumerate-information-from-ntlm-authentication/ |

## SpiderFeet project

| Resource | Path |
|----------|------|
| Skill prompt seed | `.seed/03K_Prompt_Making_for_NTLMRecon.md` |
| CLI integration table | `.seed/04_Driving and Integrating_CLI_Apps.md` |
| Local binary | `.tools/NTLMRecon/NTLMRecon` |
| Local README | `.tools/NTLMRecon/README.md` |
| Help capture | `.tmp_ntlmrecon_help/help.txt` |
| Operator CLI options | `.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md` |
| Zero to Hero | `.docs/docs-for-cli-tools/NTLMRecon-Zero-to-Hero.md` |

## Version notes

- **Captured binary** (2026-08-10): Praetorian Go build at `.tools/NTLMRecon/NTLMRecon`; live help exposes **`-t`** and **`-o`** only.
- **main**: README/source may add `-H`, `-debug`; not present on the captured release binary — verify before documenting as available.
