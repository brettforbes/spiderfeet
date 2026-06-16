# Aurelian CLI Options

## Core command shape

`aurelian <platform> <category> <module> [flags]`

Platforms:
- `aws`
- `azure`
- `gcp`

Categories:
- `recon`
- `analyze` (notably on AWS in published docs)

## Common recon modules

- `find-secrets`
- `public-resources`
- `subdomain-takeover`
- `list-all`
- AWS extras: `whoami`, `graph`, `account-auth-details`, `resource-policies`, `org-policies`

## Common scope flags

- `--subscription-id` (Azure)
- `--project-id` (GCP)
- module-specific provider flags from module docs

## Examples

```bash
aurelian aws recon whoami
aurelian aws recon find-secrets
aurelian aws recon public-resources
aurelian aws recon graph --neo4j-uri bolt://localhost:7687
aurelian azure recon find-secrets --subscription-id <id>
aurelian gcp recon public-resources --project-id <id>
aurelian list-modules
```

## Notes

- Use `aurelian list-modules` to enumerate available modules on the installed version.
- Run `aurelian <platform> <category> <module> --help` for exact module flags.
