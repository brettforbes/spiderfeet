# Pius — semantic outcome matrix (exploration redo)

**Status:** Formal examination complete (2026-06-30) — see `app_examination_docs/pius/`  
**Skill:** `.cursor/skills/pius/SKILL.md`  
**Task:** GitHub #882 · Epic #880 · Program #826

## Why prior examination failed

| Failure | Evidence |
|---------|----------|
| Sparse permissive target | Exam B `Nmap Scanme` + `scanme.nmap.org` → **1** NDJSON line (whois preseed only) |
| Missing structured files | Exams 3, 5, 6 — no `*_output_structured.jsonl` |
| Truncated terminal capture | Exam F used `head -60` in manifest (violates proj-06) |
| Wrong org for CIDR class | RIR scenarios never produced `Type: cidr` rows in saved artifacts |
| Bad capture path | Direct write to `/mnt/c/...` truncates NDJSON — must use WSL `/tmp` then copy |

## Semantic outcome classes (Pius)

| ID | Outcome class | Planned scenario key | Org + hints / plugins | Exploration status | Probe evidence |
|----|---------------|----------------------|------------------------|-------------------|----------------|
| P1 | crt-sh subdomain richness | `passive_crt_corporate_ndjson` | `Praetorian` + `--domain praetorian.com` + `crt-sh` | **Demonstrated** | `pius/praetorian_crt_rich.ndjson` — 104 `domain` rows |
| P2 | crt-sh at scale | `passive_crt_scale_ndjson` | `Linode` + `linode.com` + `crt-sh` | **Demonstrated** | probe 4142 lines (sample: `pius/linode_crt_sample.ndjson` 50 rows) |
| P3 | Corporate gleif/wikidata | `passive_gleif_corporate_ndjson` | `BBC` + `bbc.co.uk` + gleif,wikidata | **Prior exam rich** | old exam 1 had 153 lines — keep target, re-capture with WSL `/tmp` discipline |
| P4 | RIR CIDR blocks | `passive_rir_cidr_ndjson` | org with netblocks + `arin,ripe,apnic` phase-2 | **Not demonstrated** | Amazon/Linode RIR runs stopped at preseed only under 90s — needs long-run follow-up |
| P5 | whois preseed only (sparse) | `passive_sparse_ndjson` | `Nmap Scanme` + `scanme.nmap.org` | **Demonstrated** | `pius/scanme_sparse.ndjson` — 1 preseed (intentional sparse) |
| P6 | Obscure org clean miss | `passive_obscure_clean_miss` | `ZZZZ Nonexistent Org` + gleif,whois | **Not started** | schedule after capture fix |
| P7 | Keyed plugin (Shodan) | `passive_shodan_ndjson` | when `SHODAN_API_KEY` present | **Deferred** | Subscriptions / `.tools/pius.env` |
| P8 | Terminal review (full) | `passive_corporate_terminal` | BBC or Praetorian, `--output terminal` | **Not started** | **no head/tail** — full stdout capture |
| P9 | needs_review / low confidence | `passive_low_confidence_ndjson` | gleif/wikidata on BBC | **In prior exam** | filter `Data.needs_review` — re-capture |
| P10 | Active DNS mode | `active_dns_ndjson` | `--mode active` (authorized) | **Out of scope** until passive matrix complete |

## Input tuning rules (Pius)

1. **Always pass `--domain`** for the org you care about — without it crt-sh/passive-dns stay empty.
2. Use **Praetorian** or **Linode** (not scanme) to prove **domain richness**; use **BBC** for corporate/gleif/wikidata diversity.
3. Capture NDJSON via **WSL `/tmp`** then copy — never stream directly to `/mnt/c/...` from pius.
4. RIR **CIDR** rows may require **multi-minute** phase-2 completion — poll `wc -l` until stable before declaring sparse.
5. Do not use `head`/`tail` in examination commands; terminal scenarios capture full text.
6. Map plugins to semantic classes — running six plugins that all return one line is worse than three plugins that each prove a distinct `Type`.

## Recommended formal scenario set (draft)

| Key | Purpose |
|-----|---------|
| `crt_praetorian_ndjson` | Rich crt-sh domains (permissive vendor self) |
| `crt_linode_ndjson` | High-volume crt-sh (stress parser) |
| `corporate_bbc_gleif_ndjson` | gleif + wikidata + whois corporate |
| `rir_cidr_long_ndjson` | arin,ripe,apnic,edgar — **long timeout**, verify `Type:cidr` |
| `sparse_scanme_ndjson` | clean sparse / preseed-only negative |
| `obscure_miss_ndjson` | no findings |
| `corporate_bbc_terminal` | full terminal text (no truncation) |

## Next exploration steps (#882)

- [ ] Long-run RIR probe (10+ min) until `Type: cidr` demonstrated or documented blocker
- [ ] Re-capture BBC gleif/wikidata with `/tmp` discipline
- [ ] Obscure org clean miss probe
- [ ] Shodan scenario when API key available
- [ ] Rewrite `manifests/pius.yaml` from matrix
- [ ] Only then run `harvest.py`

## Web / upstream references

- [Pius attack surface blog](https://www.praetorian.com/blog/attack-surface-mapping-tool-pius/) — Acme Corp example with `[cidr]` and `[domain]` rows
- [github.com/praetorian-inc/pius](https://github.com/praetorian-inc/pius) — `--output ndjson`, plugin phases
