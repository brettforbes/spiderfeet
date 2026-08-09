# uncover Sources

Collected for skill/docs rebuild from `.seed/03V_Prompt_Making_for_uncover.md` and live binary help (**2026-08-10**, **v1.2.1**).

## Official docs & repo

- https://github.com/projectdiscovery/uncover
- https://github.com/projectdiscovery/uncover/blob/main/README.md
- https://github.com/projectdiscovery/uncover/releases
- https://docs.projectdiscovery.io/opensource/uncover/overview

## Developer references

- https://pkg.go.dev/github.com/projectdiscovery/uncover
- https://github.com/projectdiscovery/uncover/blob/main/sources/provider.go
- https://github.com/projectdiscovery/uncover/blob/main/sources/result.go (`Result` JSONL fields)

## Configuration guides

- https://github.com/projectdiscovery/uncover/discussions/3
- https://netlas.io/blog/netlas_and_uncover/

## Local evidence (this workspace)

| Artifact | Path |
|----------|------|
| Binary | `C:\projects\spiderfeet\.tools\uncover\uncover.exe` |
| Help captures | `.tmp_uncover_help/help_h.txt`, `help_long.txt`, `version.txt` |
| Skill | `.cursor/skills/uncover/SKILL.md` |
| Operator docs | `.docs/docs-for-cli-tools/uncover-Zero-to-Hero.md`, `uncover-CLI-Options.md` |

## Provider configuration (upstream README)

Default file: `$CONFIG/uncover/provider-config.yaml`  
This Windows host (from `-h`): `C:\Users\brett\AppData\Roaming\uncover\provider-config.yaml`

Example shape (keys are secrets — do not commit):

```yaml
shodan:
  - SHODAN_API_KEY_1
censys:
  - CENSYS_API_TOKEN:CENSYS_ORGANIZATION_ID
fofa:
  - FOFA_EMAIL:FOFA_KEY
# … additional engines per README
```

Environment variables (selection from README): `SHODAN_API_KEY`, `CENSYS_API_TOKEN`, `CENSYS_ORGANIZATION_ID`, `FOFA_EMAIL`, `FOFA_KEY`, `QUAKE_TOKEN`, `HUNTER_API_KEY`, `ZOOMEYE_API_KEY`, `NETLAS_API_KEY`, `CRIMINALIP_API_KEY`, `PUBLICWWW_API_KEY`, `HUNTERHOW_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_API_CX`, `ONYPHE_API_KEY`, `DRIFTNET_API_KEY`, `DAYDAYMAP_API_KEY`, `NERDYDATA_API_KEY`.

**Notes**

- Multiple keys per provider → uncover randomizes per execution.
- **`shodan-idb` does not require an API key.**
- Always capture **`uncover … -json`** for formal examination.
- Live engine list and flags: trust `.tmp_uncover_help/` over stale README snippets when they diverge.
