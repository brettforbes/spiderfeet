# Subfinder Provider Configuration

Subfinder aggregates **passive** subdomain sources (certificate transparency, APIs, search engines, etc.). Result quality depends heavily on configured API keys.

## Config file locations

| OS | Path |
|----|------|
| Linux/macOS | `~/.config/subfinder/provider-config.yaml` |
| Windows | `%APPDATA%\subfinder\provider-config.yaml` |

Override with `-pc /path/to/provider-config.yaml`.

Main config (resolvers, defaults): `config.yaml` in the same directory (`-config`).

## Example `provider-config.yaml`

```yaml
# Keys are illustrative — use your own credentials
shodan:
  - SHODAN_API_KEY_HERE
securitytrails:
  - SECURITYTRAILS_API_KEY_HERE
virustotal:
  - VT_API_KEY_HERE
github:
  - GITHUB_TOKEN_HERE
zoomeyeapi:
  - ZOOMEYE_USERNAME
  - ZOOMEYE_API_KEY
censys:
  - CENSYS_API_ID
  - CENSYS_API_SECRET
```

Not every source requires a key. Free sources (e.g. `crtsh`, `hackertarget`, `alienvault` where available) work without configuration.

## Discover available sources

```bash
subfinder -ls
```

## Source selection flags

| Flag | Use when |
|------|----------|
| `-s crtsh,hackertarget` | Fast first pass with free sources |
| `-all` | Maximum breadth; slow; API quota heavy |
| `-recursive` | Deeper enumeration on sources that recurse |
| `-es broken_source` | Provider errors or rate limits |

## API key hygiene

- Never commit `provider-config.yaml` to git.
- Rotate keys if leaked in corpus logs.
- Use `-rl` / `-rls` to avoid burning paid quotas.
- Document which keys were used in examination `manifest.json` metadata.

## Docker with local config

```bash
docker run -v $HOME/.config/subfinder:/root/.config/subfinder \
  projectdiscovery/subfinder:latest -d example.com -oJ
```

## Troubleshooting thin results

1. Run `subfinder -d example.com -v` and note failing sources.
2. Verify keys in `provider-config.yaml`.
3. Add high-yield sources (`securitytrails`, `shodan`, `virustotal`) when licensed.
4. Retry with `-all` on a single apex domain.
5. Compare against **dnsx** / **amass** passive modules for gap analysis.

## Official references

- https://docs.projectdiscovery.io/opensource/subfinder/install
- https://github.com/projectdiscovery/subfinder#post-installation-instructions
