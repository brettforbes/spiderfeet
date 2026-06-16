# Aurelian CLI Options

## Command layout

`aurelian <platform> <category> <module> [flags]`

Platforms:
- `aws`
- `azure`
- `gcp`

Categories:
- `recon`
- `analyze`

## Common modules

AWS recon:
- `whoami`
- `find-secrets`
- `public-resources`
- `graph`
- `subdomain-takeover`

Azure recon:
- `find-secrets`
- `public-resources`
- `configuration-scan`
- `subdomain-takeover`

GCP recon:
- `find-secrets`
- `public-resources`
- `subdomain-takeover`

## Common scope flags

- `--subscription-id <id>` (Azure)
- `--project-id <id>` (GCP)
- module-specific flags from module help

## Examples

```bash
aurelian aws recon whoami
aurelian aws recon find-secrets
aurelian aws recon graph --neo4j-uri bolt://localhost:7687
aurelian azure recon public-resources --subscription-id <id>
aurelian gcp recon find-secrets --project-id <id>
aurelian list-modules
```

## Notes

- Use `aurelian list-modules` to enumerate installed module names.
- Use module-level `--help` for exact flags on your version.
