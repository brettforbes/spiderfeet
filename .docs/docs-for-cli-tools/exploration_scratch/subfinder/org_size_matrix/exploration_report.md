# Subfinder exploration — org size matrix (2026-07-06)

**Mode:** Exploration only (no formal examination bundles).  
**Binary:** `.tools/bin/subfinder.exe` v2.6.8  
**Default pass:** `subfinder -d <apex> -oJ -cs -silent` (passive, source attribution)  
**Follow-up:** `subfinder -d <apex> -active -oJ -oI -cs -silent` on selected targets  

**Input rule:** Apex domain only (`k2am.com.au`, not `https://www.k2am.com.au/`).

## Summary table (passive `-cs`)

| Label | Apex | Records | Unique hosts | Sources | Semantic character |
|-------|------|---------|--------------|---------|-------------------|
| **sbs** | `sbs.com.au` | 50 | 50 | hackertarget only | **Enterprise** — deep AWS env names (`fos.*`, `phoenix.*`, `mobilelayer*`), api/auth/assets |
| **upside_au** | `theupside.com.au` | 26 | 26 | crtsh + hackertarget | **Medium-rich** — dev/test/k8s/mail/newsletter, heavy `www.*` doubling |
| **k2am** | `k2am.com.au` | 18 | 18 | crtsh + hackertarget | **Medium** — classic hosting panel (`cpanel`, `webmail`, `owa`, `apps`) |
| **upside_com** | `theupside.com` | 12 | 12 | crtsh + hackertarget | **Medium-sparse** — blog, international, uat, marketing subs |
| **squarepeg** | `squarepeg.vc` | 7 | 7 | crtsh + hackertarget | **Small VC rich** — `data`, `helix`, event/campaign subs |
| **vcof** | `venturecapitalopportunitiesfund.com.au` | 1 | 1 | crtsh + hackertarget | **Ultra-sparse** — apex `www` only |

Runtime: ~3–22 s per domain on free passive sources (no API keys observed in provider config).

## Semantic output shapes observed

### Passive + `-cs`

```json
{"host":"dev.theupside.com.au","input":"theupside.com.au","sources":["crtsh","hackertarget"]}
```

- Field is **`sources`** (array); multiple provenance per host when corroborated.
- No `ip` — hosts are **INTERNET_NAME_UNRESOLVED** until dnsx/active.

### Active + `-oI` + `-cs`

```json
{"host":"data.squarepeg.vc","ip":"104.21.85.245","input":"squarepeg.vc","source":"hackertarget"}
```

- Field is **`source`** (string), not `sources` — **different JSON shape** (examination-worthy).
- Adds **`ip`** → enables `INTERNET_NAME` + `IP_ADDRESS` nugget edges.
- **Filters** unresolved names: k2am 18→8, upside_au 26→22 (cpanel/webdisk-style ghosts dropped).

### Clean miss

- `not-a-real-domain-xyzzy.invalid` → `records: []`, exit 0 (valid empty scan, not a hard error).

### Proven sparse (vcof)

- crtsh-only second pass still **1 host** — limitation is target footprint, not source choice.

## Size-tier interpretation

| Tier | Example | Examination utility |
|------|---------|---------------------|
| Enterprise | `sbs.com.au` | Not a “small site” — use as **large-org contrast** (volume + deep labels). User listed it; keep as upper bound, not SME exemplar. |
| Medium-rich SME | `theupside.com.au` | **Best primary rich examination** — env hints (dev/test/k8s), multi-source rows, 26 hosts. |
| Medium hosting-style | `k2am.com.au` | **Strong examination** — aligns with pius corporate_k2am; diverse infra prefixes. |
| Small VC | `squarepeg.vc` | **Strong small-org examination** — few hosts but distinct semantics (data platform, summit campaign). |
| Related TLD sibling | `theupside.com` | **Good pair** with `.com.au` — shows brand split across zones (12 vs 26). |
| Near clean-miss | `venturecapitalopportunitiesfund.com.au` | **Best sparse examination** — single `www` row; documents “org exists but passive enum is empty”. |

## Recommended formal examination scenarios

| Priority | Scenario id (proposed) | Command family | Rationale |
|----------|------------------------|----------------|-----------|
| P0 | `corporate_upside_au_passive_cs` | passive `-oJ -cs` | Richest SME pass; multi-source array shape |
| P0 | `corporate_squarepeg_passive_cs` | passive `-oJ -cs` | Small org with meaningful host variety |
| P0 | `corporate_vcof_sparse_passive` | passive `-oJ -cs` | Near clean-miss / ultra-sparse |
| P1 | `corporate_k2am_passive_cs` | passive `-oJ -cs` | Medium AU org; pairs with pius K2 line |
| P1 | `corporate_k2am_active_oI` | active `-oJ -oI -cs` | IP + singular `source` shape; resolved subset |
| P1 | `corporate_upside_com_passive_cs` | passive `-oJ -cs` | TLD variant / sparser sibling zone |
| P2 | `enterprise_sbs_passive_cs` | passive `-oJ -cs` | Enterprise volume (optional 7th slot) |
| P2 | `invalid_domain_clean_miss` | passive on bogus apex | Empty `records[]` with exit 0 |

**Defer / skip for corpus:** none — all six user domains produced usable semantic classes. K2 (`k2am.com.au`) is online here (18 hosts); pius K2 was deferred separately.

## Gaps / follow-up before harvest

1. Configure `provider-config.yaml` API keys — expect richer counts on upside/sbs with SecurityTrails/Shodan etc.
2. Add **dnsx** chain scenario after passive (wildcard filter) — not explored in this pass.
3. Document passive `sources[]` vs active `source` + `ip` in `subfinder` structured converter.
4. **bbc.co.uk** or similar still useful as CDN corporate negative — not in this matrix.

## Artifacts

```
.docs/docs-for-cli-tools/exploration_scratch/subfinder/org_size_matrix/
  *_passive_cs.jsonl
  *_active_oI.jsonl
  summary.json
  exploration_report.md
```
