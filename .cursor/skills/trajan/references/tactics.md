# Trajan Tactics

## Recommended sequencing

1. **Token whoami** — `enumerate token` (or Jenkins `enumerate access`) with `-o json`.
2. **Inventory** — repos/projects/jobs relevant to ROE.
3. **Single-target scan** — one `--repo` / `--project` / job; validate JSON schema assumptions.
4. **Detector tuning** — `--list`, then `--severity` / `--capabilities` for focused passes.
5. **Expand** — org/group/folder sweeps with bounded `--concurrency`.
6. **Offline gap-fill** — `--path` when API access is partial.
7. **Offensive verify (optional)** — only with written ROE: `attack --dry-run` → `--confirm` → `retrieve` / `cleanup`.
8. **Remediation loop** — re-scan changed workflows; differential against prior JSON.

## Tactics by goal

### Maximize rich findings (permissive lab / intentional vuln CI)

- Prefer API mode with a token that can read workflows, secrets metadata, and runners.
- Enable `--detailed`; avoid over-filtering severity on the first pass.
- On GitHub, combine `scan` with `search` for self-hosted runners, then scan hits.
- Use `--capabilities` only after a full pass shows which detectors fire.

### Sparse / hardened org

- Expect empty or low-severity finding lists — still valid JSON for clean-miss scenarios.
- Lower `--concurrency`; respect rate limits; split orgs.
- Offline `--path` on checked-out workflow trees when API is denied.

### Thin yield

- Confirm token scopes via enumerate.
- Try alternate scope flags (`--user` vs `--org`, GitLab `--group` vs `--project`).
- GHES / self-hosted: set `--url` correctly.
- Jenkins: ensure `--url` points at a live instance for access/CSRF checks.
- JFrog: pass both `--secrets` and `--token-info`.

### Offensive (gated)

- Never default corpus scenarios to live `attack`.
- Always `--dry-run` first; require `--confirm` for execution.
- Prefer single `--plugin` over `--all` or named `--chain` until impact is understood.
- Track `--session` for cleanup; run `attack cleanup` when available.
- Redact all retrieve/attack artifacts before sharing or graphing.

## Practical triage order

1. Secret / token exposure and PPE / pwn-request class findings
2. Self-hosted runner / agent exec paths
3. Artifact / cache poisoning and supply-chain injection
4. Excessive permissions / review bypass / TOCTOU
5. Unpinned actions and hardening gaps

## Pipeline with sibling tools

```text
trajan scan (-o json)  →  pipeline abuse findings
titus scan / report    →  secret content in repo/history
```

Do not substitute Titus for Trajan or vice versa.
