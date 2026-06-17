# PIUS Tactics — Adaptive Discovery Sequences

## Tactic 1: Passive baseline with domain hint

**Goal:** Maximum domains + RIR CIDRs without target DNS probes.

```bash
pius run --org "Acme Corporation" --domain acme.com --output ndjson
```

**Adapt:**

- Few domains → set API keys (`SECURITYTRAILS`, `VIEWDNS`, `APOLLO`)
- Few CIDRs → Tactic 2 (org spelling) or Tactic 3 (RIR-only plugins)

## Tactic 2: Org name variants

**When:** Phase 1 finds no handles.

Try sequentially:

```bash
pius run --org "Acme Corporation" --domain acme.com --plugins whois,edgar --output ndjson
pius run --org "Acme Corp" --domain acme.com --plugins whois,edgar --output ndjson
pius run --org "Acme Inc" --domain acme.com --plugins whois,edgar --output ndjson
```

Compare CIDR overlap before merging.

## Tactic 3: RIR-focused CIDR discovery

**When:** Need netblocks for scanning; domains secondary.

```bash
pius run --org "Acme Corporation" \
  --plugins whois,edgar,arin,ripe,apnic,afrinic,lacnic \
  --output ndjson
```

**Adapt:**

- US-heavy org → `--plugins whois,arin` for speed
- EU-heavy → add `ripe` first

## Tactic 4: ASN shortcut

**When:** Known ASN from BGP/WHOIS.

```bash
pius run --org "Acme Corp" --asn AS12345 --plugins asn-bgp --output ndjson
```

Bypasses handle resolution for announced prefixes.

## Tactic 5: Active DNS expansion (authorized)

**When:** Passive sources exhausted; engagement allows DNS traffic.

```bash
pius run --org "Acme Corp" --domain acme.com --mode active --output ndjson
```

Or surgical:

```bash
pius run --domain acme.com --mode active --plugins dns-brute,doh-enum --output ndjson
```

## Tactic 6: Confidence-filtered export

**When:** Noisy `needs_review` rows pollute scope.

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -c 'select(.Data.needs_review != true)' > high_conf.ndjson
```

Review queue:

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -c 'select(.Data.needs_review == true)'
```

## Tactic 7: Downstream tool chains

### Domains → web stack

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -r 'select(.Type=="domain") | .Value' \
  | while read h; do wafw00f -a -o- -f json "https://$h"; done
```

### CIDRs → port scan → Nerva

```bash
pius run --org "Acme" --output ndjson \
  | jq -r 'select(.Type=="cidr") | .Value' > cidrs.txt
# feed cidrs.txt to naabu/nmap/nerva per operator runbook
```

### Domains → Nuclei

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -r 'select(.Type=="domain") | "https://" + .Value' > urls.txt
```

## Tactic 8: Plugin cost control

**When:** Rate limits or slow runs.

```bash
# Reduce parallelism
pius run --org "Acme" --domain acme.com --concurrency 2 --output ndjson

# Minimal plugin set
pius run --org "Acme" --domain acme.com --plugins crt-sh,gleif,whois,arin --output ndjson

# Disable expensive/noisy
pius run --org "Acme" --disable edgar,github-org,google-dorks --output ndjson
```

## Tactic 9: Cache refresh

**When:** APNIC/AFRINIC results stale (>24h).

```bash
rm -rf ~/.pius/cache/
pius run --org "Acme Corp" --output ndjson
```

## Tactic 10: SpiderFeet investigation flow

```
1. Manual or module seed: COMPANY_NAME / operator org string
2. pius run --output ndjson
3. Import domains → INTERNET_NAME events
4. Import cidrs → NETBLOCK_OWNER events
5. Enable sfp_tool_wafw00f, sfp_tool_cmseek on INTERNET_NAME
6. Nuclei/Nmap modules on expanded surface
```

## Decision matrix

| Symptom | Action |
|---------|--------|
| Zero domains, no `--domain` | Add `--domain` |
| Zero CIDRs | Check Phase 1 with `--plugins whois` only |
| Only `needs_review` domains | Refine org string; add domain hint |
| Duplicate domains | Dedupe on ingest (same `Value`) |
| Cloud-only org | Expect few RIR CIDRs; rely on CT/passive DNS |
