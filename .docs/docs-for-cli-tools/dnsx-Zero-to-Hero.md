# dnsx Zero to Hero — DNS Resolution, JSONL, and Nuggets

From install to orchestrated recon with **`dnsx -json`**, nugget mapping, and pipelines to **httpx** and **naabu**.

Skill reference: `.cursor/skills/dnsx/SKILL.md`

**Binary (this repo):** `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe` — **v1.2.3** (help captured **2026-08-10**).

## What dnsx does

dnsx is ProjectDiscovery's **fast DNS toolkit**: it takes hostnames, domains + wordlists, or stdin and runs concurrent DNS probes (A/AAAA/CNAME/MX/TXT/…), with wildcard filtering and JSONL export.

dnsx does **not**:

- Enumerate subdomains passively (use **subfinder**)
- Probe HTTP (use **httpx**)
- Port-scan (use **naabu** / **nmap**)
- Run vulnerability templates (use **nuclei**)

---

## Level 0 — Install

```bash
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
dnsx -version
```

Or: https://github.com/projectdiscovery/dnsx/releases

This workspace: `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe`

---

## Level 1 — First resolve

```bash
echo scanme.nmap.org | dnsx -silent -a
```

With answers in the line:

```bash
echo scanme.nmap.org | dnsx -silent -a -resp
```

---

## Level 2 — A + AAAA validation list

```bash
dnsx -l hosts.txt -a -aaaa -silent
```

Keep only names that answer — feed those to httpx/naabu.

---

## Level 3 — JSONL for automation

```bash
dnsx -l hosts.txt -a -aaaa -json -o results.jsonl
```

Example line:

```json
{"host":"scanme.nmap.org","a":["45.33.32.156"],"aaaa":["2600:3c01::f03c:91ff:fe18:bb2f"],"status_code":"NOERROR"}
```

Compact (no raw RR dump):

```bash
dnsx -l hosts.txt -a -aaaa -json -omit-raw -o compact.jsonl
```

**Always prefer `-json` for SpiderFeet** — parse line by line into harvest `records[]`.

---

## Level 4 — Record enrichment

```bash
dnsx -l live.txt -cname -ns -mx -txt -soa -caa -json -silent -o enrich.jsonl
```

| Goal | Flags |
|------|--------|
| Aliases / SaaS | `-cname` |
| Mail / SPF | `-mx -txt` |
| Authority | `-ns -soa` |
| Broad dump | `-all` or `-recon` (noisy) |

---

## Level 5 — Filters and RCODE

```bash
dnsx -l hosts.txt -a -rcode noerror -json -silent
dnsx -l hosts.txt -a -rtf cname -json -silent
dnsx -l hosts.txt -a -resp -json -silent
```

---

## Level 6 — Wildcards and resolvers

```bash
dnsx -l candidates.txt -a -aaaa -json -auto-wildcard -wt 5
dnsx -l candidates.txt -a -json -wd example.com
dnsx -l hosts.txt -a -json -r 1.1.1.1,8.8.8.8
```

Notes from help:

- `-wd` and `-auto-wildcard` are **mutually exclusive**
- With `-wd`, other flags may be ignored — **JSON recommended**
- `-stream` disables wordlist, wildcard, stats, and stop/resume

---

## Level 7 — Bruteforce

```bash
dnsx -d example.com -w wordlist.txt -a -aaaa -json -silent -auto-wildcard -o brute.jsonl
```

Validate hits again before treating them as production hosts.

---

## Level 8 — Pipelines

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa -json
subfinder -d example.com -silent | dnsx -silent -a -aaaa | httpx -json -silent
subfinder -d example.com -silent | dnsx -silent -a | naabu -json -silent
dnsx -l ips.txt -ptr -json -silent
```

---

## Level 9 — SpiderFeet nuggets

Map JSONL → graph (`nodes[]` / `edges[]`):

| Signal | Nugget |
|--------|--------|
| `host` | `INTERNET_NAME` |
| `a` / `aaaa` | `classify_ip` → IPv4 / IPv6 types |
| SPF TXT | `DNS_SPF` |
| Other TXT | `DNS_TEXT` |
| SRV | `DNS_SRV` |
| NS / CDN labels | `PROVIDER_DNS` / `PROVIDER_HOSTING` when applicable |

Full mapping: `.cursor/skills/dnsx/references/nugget-mapping.md`

---

## Tactics for better results

- Start narrow (`-a -aaaa`), then enrich hits only.
- Use wildcard controls on brute and noisy zones.
- Differential-check with alternate `-r` lists when answers look wrong.
- Lower `-t` / set `-rl` under resolver pressure; raise `-retry` / `-timeout` on lossy networks.
- Prefer staged scenarios in corpus work over one giant `-all` run.

---

## Common pitfalls

- Parsing text banners instead of **`-json`**
- Inventing flags not in `dnsx -h`
- Treating SERVFAIL like NXDOMAIN
- Ignoring wildcards during bruteforce
- Emitting IPv6 as `IP_ADDRESS` without `classify_ip`
- Using `-stream` when you still need `-auto-wildcard` or `-resume`

---

## Next references

- `.cursor/skills/dnsx/SKILL.md`
- `.cursor/skills/dnsx/references/SKILLS.md`
- `dnsx-CLI-Options.md` (includes **Captured help**)
- [dnsx usage docs](https://docs.projectdiscovery.io/opensource/dnsx/usage)
