# Trajan CLI Options

## Core pattern

`trajan <platform> scan [scope flags] [runtime flags] [output flags]`

Platforms in public docs: `github`, `gitlab`, `ado`, `jenkins`, `jfrog`.

## Common scan flags

- `--repo <owner/repo>`: target a single repository/project.
- `--org <name>` or `--group <name>`: scan wider organization scope.
- `--path <file-or-dir>`: local workflow scan without API enumeration.
- `--concurrency <n>`: tune parallel workers.
- `--timeout <duration>`: bound scan runtime.
- `-o json`: machine-readable output for downstream parsers.

## Token and auth expectations

- GitHub PAT: `repo` for private repositories, `public_repo` for public-only.
- GitLab, Azure DevOps, Jenkins auth via provider-specific token env variables.
- Prefer env vars over inline tokens in shell history.

## High-value command examples

```bash
trajan github scan --repo owner/repo -o json
trajan github scan --org myorg --concurrency 20 -o json
trajan gitlab scan --group mygroup -o json
trajan ado scan --org myorg --repo myproject/myrepo -o json
trajan github scan --path ./.github/workflows -o json
```

## Notes

- Use `trajan <platform> --help` and `trajan <platform> scan --help` for exact installed flags.
- Prefer JSON outputs for automation; table output is for human triage.
