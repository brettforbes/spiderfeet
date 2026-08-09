# Trajan Platforms (v1.0.2)

Capabilities below are from live `--help` on **1.0.2** (2026-08-10 capture). Do not assume README “coming soon” tables override the binary.

## Summary

| Platform | Enumerate | Scan | Attack | Retrieve | Search | Notes |
|----------|-----------|------|--------|----------|--------|-------|
| `github` | yes | yes | yes | yes | yes | Fullest surface; GHES via `--url` |
| `gitlab` | yes | yes | yes | — | — | Self-hosted via `--url` |
| `ado` | yes | yes | yes | yes | — | PAT + optional Entra bearer |
| `bitbucket` | yes (token) | — | — | — | — | Enumerate-only in this build |
| `jenkins` | yes | yes | yes* | — | — | Basic auth; live URL for instance checks |
| `jfrog` | — | yes | — | — | — | `--secrets` / `--token-info`; not pipeline YAML CVE scan |

\* Jenkins parent help lists `attack`; nested attack help was not in the capture set — run `trajan jenkins attack --help` before use.

## GitHub

**Commands:** `enumerate` (`token`, `repos`, `secrets`), `scan`, `attack` (+ `cleanup`), `retrieve`, `search`.

**Auth:** `--token` or `GH_TOKEN` / `GITHUB_TOKEN`. GHES: `--url https://github.example.com/api/v3`.

**Scan targets:** `--repo owner/repo`, `--org`, `--user`, or `--path` offline.

**Search providers:** `-p github` (token) or `-p sourcegraph` (no auth per help).

**Attack plugins (help):** `secrets-dump`, `workflow-injection`, `pr-attack`, `runner-on-runner`, `interactive-shell`, `c2-setup`, `persistence`. Chains: `ror`, `secrets`, `persistence`, `full`, `ai-takeover`, `supply-chain`, `toctou-exploit`, `stealth`. Always `--dry-run` then `--confirm`.

## GitLab CI

**Commands:** `enumerate` (`token`, `projects`, `groups`, `secrets`, `branch-protections`, `runners`), `scan`, `attack`.

**Auth:** `--token` or `GITLAB_TOKEN` / `GL_TOKEN`. Self-hosted: `--url`.

**Scan targets:** `--project group/project`, `--group`, `--user`, or `--path` offline.

**Attack plugins (help):** `secrets-dump`, `runner-exec`. Flags include `--runner-tags`, `--command`, `--no-cleanup`.

## Azure DevOps

**Commands:** `enumerate` (many resource subcommands + `search`, `fork-security`, `attack-paths`), `scan`, `attack` (+ `cleanup`), `retrieve`.

**Auth:** `--token` or `AZURE_DEVOPS_PAT` / `AZDO_PAT`; `--azure-bearer-token` / `AZURE_BEARER_TOKEN` for Entra flows (required for some persistence ops per attack help).

**Scan targets:** `--org` (name or URL), `--repo project/repo`, or `--path` offline.

**Attack plugins (help):** `ado-secrets-dump`, `ado-pipeline-injection`, `ado-pr-attack`, `ado-extract-connections`, `ado-extract-securefiles`, `ado-privesc`, `ado-persistence`, `ado-agent-exec`, `ado-ai-probe`.

## Bitbucket

**Commands:** `enumerate token` only.

**Auth:** `--token` + `--email` (`BITBUCKET_EMAIL` / `BB_EMAIL`) + `--workspace` (`BITBUCKET_WORKSPACE`).

No `scan` / `attack` in 1.0.2 parent help. Captured `bitbucket scan --help` returned the parent help (no scan subcommand).

## Jenkins

**Commands:** `enumerate` (`access`, `jobs`, `nodes`, `plugins`), `scan`, `attack` (listed on parent).

**Auth:** `--username` / `--password` (`JENKINS_USERNAME` / `JENKINS_PASSWORD`).

**Scan:** `--url` for instance; `--repo` job; `--org` folder; `--path` offline (skips live anonymous/CSRF/script-console checks).

## JFrog

**Commands:** `scan` only (`--secrets`, `--token-info`).

**Auth:** `--token` / `JFROG_TOKEN` or `-u`/`-p`; `--url` instance.

Captured `jfrog enumerate --help` returned the parent help (no enumerate subcommand). Help states JFrog does not support vulnerability scanning of CI/CD pipelines.
