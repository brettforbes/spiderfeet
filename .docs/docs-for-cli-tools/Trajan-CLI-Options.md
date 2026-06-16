# Trajan CLI Options

## Command shape

`trajan <platform> scan [flags]`

Supported platforms in docs: `github`, `gitlab`, `ado`, `jenkins`, `jfrog`.

## Scope flags

- `--repo <owner/repo>`: single repository target
- `--org <org>` / `--group <group>`: broader inventory
- `--path <path>`: local workflow scanning

## Runtime flags

- `--concurrency <n>`: worker parallelism
- `--timeout <duration>`: scan time bound

## Output flags

- `-o json`: machine-readable output

## Examples by scenario

```bash
# GitHub repo
trajan github scan --repo owner/repo -o json

# GitHub org
trajan github scan --org myorg --concurrency 20 -o json

# GitLab group
trajan gitlab scan --group mygroup -o json

# Azure DevOps repo
trajan ado scan --org myorg --repo project/repo -o json

# Offline local workflows
trajan github scan --path ./.github/workflows -o json
```

## Auth reminders

- GitHub private repos need PAT `repo`.
- Public-only GitHub scanning can use `public_repo`.
- Keep tokens in environment variables, not inline arguments.

## Operator note

Run `trajan --help`, `trajan <platform> --help`, and `trajan <platform> scan --help` on the installed binary for exact version-specific flags.
