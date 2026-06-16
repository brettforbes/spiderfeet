# Trajan Zero to Hero

Trajan is a CI/CD security scanner for discovering exploitable pipeline weaknesses across GitHub Actions, GitLab CI, Azure DevOps, Jenkins, and JFrog.

## 1) Install

```bash
go install github.com/praetorian-inc/trajan/cmd/trajan@latest
```

## 2) First successful scan

```bash
export GH_TOKEN="..."
trajan github scan --repo owner/repo -o json > trajan-results.json
```

## 3) Read findings

Focus on:
- severity
- workflow file
- detection type
- evidence

Start with findings that can directly expose secrets or deploy untrusted code.

## 4) Expand safely

```bash
trajan github scan --org myorg --concurrency 20 -o json > trajan-org.json
```

Use staged rollout: one repo -> critical repos -> full org.

## 5) Offline mode

```bash
trajan github scan --path ./.github/workflows -o json > trajan-local.json
```

Use this when API access is limited; mark results as partial coverage.

## 6) Convert to SpiderFeet-style nuggets

Build `nodes` and `edges` arrays:
- Nodes: repository, workflow file, finding, risk category
- Edges: contains workflow, workflow triggers finding, finding enables risk

## 7) Operational playbook

1. baseline scan
2. parser validation
3. org sweep
4. remediation tracking
5. differential re-scan after changes

## 8) Common mistakes

- treating local path mode as equivalent to API mode
- failing to redact secrets from shared reports
- ignoring non-fatal scan errors that indicate coverage gaps

## 9) Useful references

- `.cursor/skills/trajan/references/SKILLS.md`
- `Trajan-CLI-Options.md`
