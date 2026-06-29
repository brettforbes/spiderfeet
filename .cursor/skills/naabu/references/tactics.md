# Naabu Tactics — Adaptive Port Scanning

## Maximize data on unknown networks

1. **Start narrow** — `-top-ports 100` or explicit web/admin port set before `-p -`.
2. **Host discovery** — `-wn` on /16+; extract live hosts to file for phase 2.
3. **Verify** — `-verify` on suspiciously noisy results to drop false positives.
4. **Smart scan** — `-ss` when enabled (not with `-stream`) for predictive ports.
5. **JSON always** — `-json -o phase.jsonl` per attempt; compare runs.
6. **Downstream** — httpx on 80/443/8080; Nerva on all open; Julius on AI ports.

## Hostile / filtered / CDN networks

| Situation | Tactic |
|-----------|--------|
| CDN front (Cloudflare, Akamai, …) | `-ec` limits to 80/443; use `-cdn` to label |
| Rate limiting / IDS | Lower `-rate` (100–300), increase `-timeout`, reduce `-c` |
| SYN blocked | `-s c` CONNECT scan |
| All ports filtered | Try `-passive` for historical InternetDB ports |
| API-only hosts | Focus `-p` on 443,8080,8443,3000 — see Dana Epp API scanning article |
| Local workstation scan | Default VPS rates too aggressive — `-rate 300 -c 10` |
| IPv6-only assets | `-iv 6` |
| Multi-homed DNS | `-sa` scan all resolved IPs |

## Passive vs active

| Mode | When |
|------|------|
| `-passive` | Stealth recon, compare with active later |
| Active SYN | Authorized internal/VPS scan, speed priority |
| Active CONNECT | Non-root, firewalled egress |

Passive does not replace active validation — merge unique ports from both JSONL files.

## Bug bounty / external recon chain

```
subfinder → dnsx → naabu -top-ports 1000 -json → httpx → nuclei
                              ↓
                         nerva (service ID)
```

For API servers: prioritize 443, 8443, 8080, 3000, 5000 before full port sweep.

## Corporate / protected targets

- Use **corporate seed** in formal examination — expect fewer ports, CDN exclusion.
- Document **clean miss** when zero ports (valid negative).
- Do not run `-p -` on entire corp /8 — module policy may cap netblock size.

## When to escalate to Nmap

| Naabu result | Next step |
|--------------|-----------|
| Open 22,80,443 only | `nmap -sV -O` on those ports |
| Many open ports | `-nmap-cli 'nmap -sV --open'` or separate Nmap XML phase |
| Need NSE scripts | Nmap `--script`, not naabu alone |
| OS fingerprint required | Nmap `-O` after naabu port list |

## When to stop escalating

- Sufficient open ports for investigation goal.
- Repeated false positives after `-verify`.
- Scope time budget exhausted on `-p -`.

## Negative / clean miss

```bash
naabu -host example.com -p 65534 -json -silent
# empty output = clean miss for SpiderFeet negative fixture
```
