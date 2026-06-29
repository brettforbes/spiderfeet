# Bootstrap Blockers

**Run:** 2026-05-23-init

## B1 — GitHub Project API scope

| Field | Value |
|-------|--------|
| State | `blocked-with-tracked-issue` |
| Impact | Cannot list/adopt/normalize canonical VibeGov board |
| Evidence | `gh project list` → missing `read:project` scope |
| Remediation | `gh auth refresh -s project` then bootstrap **update** |

## B2 — GitHub Issues disabled

| Field | Value |
|-------|--------|
| State | `blocked-with-tracked-issue` |
| Impact | Cannot import/link issues to project board |
| Evidence | `gh issue list` → repository has disabled issues |
| Remediation | Enable Issues in repo Settings **or** document file-only backlog as canonical (operator decision) |

## B3 — Branch protection not verified

| Field | Value |
|-------|--------|
| State | degraded verification |
| Impact | Protection rules unknown |
| Remediation | Push `develop`, then verify per `.github/branch-protection-checklist.md` |

## B4 — WSL cannot ARP-scan physical LAN (netdiscover blocked)

| Field | Value |
|-------|--------|
| State | `degraded` — mirrored networking failed 2026-06-29 (`ConfigureNetworking/0x8007054f`, fallback to `networkingMode None`) |
| Impact | WSL `netdiscover` harvest blocked; use `windows-lan` runtime in manifest v6 |
| Evidence | `wsl ip -br link` shows only `lo`; exams 6–10 captured `eth1: No such device` |
| Workaround | `run_netdiscover_lan.ps1` via `harvest.py` `windows-lan` runtime (exams 11–15) |
| Remediation | Reboot / `setup_wsl_lan_network.ps1`; then restore `wsl-root` + `-i eth1` in manifest |


- Dirty working tree — recorded, not resolved (commit policy forbidden)
- Product implementation — intentionally stopped per bootstrap gate
