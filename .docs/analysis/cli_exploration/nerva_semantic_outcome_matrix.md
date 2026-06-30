# Nerva — semantic outcome matrix (exploration redo)

**Status:** Formal examination complete (2026-06-30) — see `app_examination_docs/nerva/`  
**Skill:** `.cursor/skills/nerva/SKILL.md`  
**Task:** GitHub #881 · Epic #880 · Program #826

## Why prior examination failed

| Failure | Evidence |
|---------|----------|
| Missing structured artifacts | Exams 4–6: no `*_output_structured.jsonl` on disk |
| Shallow option matrix | Six scenarios on scanme only; no `--misconfigs`, no `-l` list file, no HTTPS-rich target |
| Wrong empty semantics | `scanme.nmap.org:443` and `:1` runs produced no JSON — not captured as distinct scenarios with evidence |
| Pipeline violation | Nerva used without verified open ports from upstream scan list (acceptable for scanme:22/80 but not documented) |

## Semantic outcome classes (Nerva)

| ID | Outcome class | Planned scenario key | Target / command family | Exploration status | Probe evidence |
|----|---------------|----------------------|-------------------------|-------------------|----------------|
| N1 | TCP HTTP rich metadata | `tcp_http_rich_json` | `scanme.nmap.org:80 --json` | **Demonstrated** | `nerva/tcp_http.jsonl` — 2 lines, `technologies`, `cpes` |
| N2 | TCP SSH rich + security findings | `tcp_ssh_misconfigs_json` | `scanme.nmap.org:22 --json --misconfigs` | **Demonstrated** | `nerva/tcp_ssh_misconfigs.jsonl` — `security_findings[]`, host keys |
| N3 | TCP HTTPS / TLS rich | `tcp_https_corporate_json` | `praetorian.com:443 --json --misconfigs` | **Demonstrated** | `nerva/tcp_https_praetorian.jsonl` — 4 lines (v4+v6) |
| N4 | Multi-target comma list | `tcp_multi_comma_json` | `-t scanme:22,scanme:80,scanme:443` | **Partial** | `nerva/tcp_multi.jsonl` — ssh+http only (443 empty on scanme) |
| N5 | Target list file (`-l`) | `tcp_list_file_json` | `targets.txt` scanme:22/80 + praetorian:443 | **Demonstrated** | `nerva/tcp_list_file.jsonl` — 8 lines, 3 protocols |
| N6 | Fast mode | `tcp_fast_https_json` | `--fast` on known-open HTTPS | **Blocked** | scanme:443 empty — retry on `praetorian.com:443` |
| N7 | Human-readable stdout | `tcp_http_human_text` | no `--json` | **Demonstrated** | `nerva/human_80.stdout` — `http://host:port (ip)` lines |
| N8 | Clean miss (closed port) | `tcp_closed_clean_miss` | `scanme.nmap.org:1 --json` | **Demonstrated** | empty JSONL + zero stdout JSON (valid miss) |
| N9 | UDP fingerprint | `udp_dns_json` | `-U` e.g. `8.8.8.8:53` | **Not started** | requires admin / dedicated target |
| N10 | CSV export | `tcp_csv_export` | `--csv -o` | **Not started** | alternate structured family |
| N11 | Unknown / timeout | `tcp_slow_timeout` | high `-w` on latent port | **Not started** | tune after N1–N8 stable |

## Input tuning rules (Nerva)

1. **Never examine a port without confirming it is open** (Nmap `-p`, Naabu, or known permissive host).
2. Use **praetorian.com:443** (or similar) when scanme HTTPS is empty — do not treat “no JSON” as tool failure without target swap.
3. Always include **`--misconfigs`** on SSH (and HTTPS where supported) to surface `security_findings` as a distinct field family.
4. Prefer **`-l targets.txt`** for multi-host scenarios (pipeline realism after Nmap grep).
5. Record **stderr** separately; do not mix into JSONL.

## Next exploration steps (#881)

- [ ] Complete N6 fast mode on `praetorian.com:443`
- [ ] Run N9 UDP on `scanme.nmap.org:53` or resolver with `-U` (+ sudo note)
- [ ] Draft `.strategy/nerva_strategy.skill` after all rows demonstrated or documented impossible
- [ ] Rewrite `manifests/nerva.yaml` from this matrix (not from archetype A–F letters)
- [ ] Only then run `harvest.py`

## Web / upstream references

- [Praetorian Nerva blog](https://www.praetorian.com/blog/whats-running-on-that-port-introducing-nerva-for-service-fingerprinting/) — pipeline + JSON
- [github.com/praetorian-inc/nerva](https://github.com/praetorian-inc/nerva) — `--json`, `-l`, `--misconfigs`, `-U`
