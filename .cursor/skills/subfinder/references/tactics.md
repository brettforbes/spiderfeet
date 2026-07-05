# Subfinder Tactics — Maximize Enumeration

Adapt technique when networks, providers, or DNS defenses reduce yield.

## Thin passive results

1. **Verify provider config** — `provider-config.yaml` keys for Shodan, SecurityTrails, VirusTotal, etc.
2. **Verbose pass** — `subfinder -d DOMAIN -v` to see failing sources; `-es` broken ones.
3. **Widen sources** — `-s crtsh,hackertarget,alienvault,securitytrails` then `-all` on apex only.
4. **Recursive sources** — `-recursive` for deep discovery on providers that support it.
5. **Increase budget** — `-max-time 30 -timeout 60`.
6. **Cross-check** — compare with `amass`, `assetfinder`, or SpiderFeet `sfp_sublist3r` for gaps.

## Rate limits and API blocks

1. Lower global rate: `-rl 5`.
2. Per-provider: `-rls "hackertarget=10/s,shodan=15/s"`.
3. Exclude noisy/blocked: `-es zoomeyeapi,alienvault`.
4. Stagger batch domains in `-dL` across runs.
5. Use paid API tiers only on prioritized apex domains.

## Wildcard and sinkhole DNS

Subfinder passive lists may include wildcard-generated names.

1. Pipe to **dnsx** with wildcard detection (version-dependent flags).
2. Use `-active` to drop non-resolving names.
3. Compare random label probes (`random12345.example.com`) before trusting rare subdomains.
4. Do not port-scan unvalidated wildcard hosts.

## Defensive / hardened organizations

1. Expect fewer CT/API leaks — combine passive + active DNS brute (**dnsx** wordlist) as separate phase.
2. Use `-m` for high-value patterns (`api`, `vpn`, `citrix`, `autodiscover`).
3. Chain **httpx** before **nuclei** to avoid scanning non-HTTP noise.
4. Document **clean_miss** when authorized apex returns zero subs after full passive + active — valid negative fixture.

## Maximize downstream data

| Stage | Tactic |
|-------|--------|
| Subfinder | `-oJ -cs` for provenance |
| dnsx | `-a -aaaa -cname -resp -j` |
| httpx | `-title -tech-detect -status-code` |
| naabu | `-top-ports 1000` on live IPs only |
| nuclei | tag-targeted after httpx tech fingerprint |

## Source tiering (recommended order)

1. **Tier 0 (free, fast):** `crtsh`, `hackertarget`, `alienvault`
2. **Tier 1 (API keys):** `securitytrails`, `shodan`, `virustotal`, `github`
3. **Tier 2 (breadth):** `-all` or remaining `-ls` sources
4. **Tier 3 (validation):** `-active -oI` or dnsx

## When to stop adapting

- Authorized scope fully enumerated and dnsx-validated.
- API quotas exhausted for the session (record in manifest).
- Duplicate FQDN set stable across two widening passes.

## Anti-patterns

- Running `-all` on dozens of domains without rate limits.
- Treating passive JSONL as confirmed live hosts without dnsx.
- Scanning out-of-scope sibling domains discovered via CT leaks.
- Committing API keys to examination artifacts.
