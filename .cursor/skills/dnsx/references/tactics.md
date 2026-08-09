# dnsx Tactics — Maximize DNS Evidence

## Thin or empty JSONL

1. **Validate upstream list** — Passive names from subfinder may be stale; empty output can be a valid clean miss.
2. **Add AAAA** — IPv6-only hosts disappear if you only query `-a`.
3. **Retry / timeout** — Raise `-retry` (default 2), `-timeout` (default 3s).
4. **Lower concurrency** — Drop `-t` when resolvers throttle; optionally set `-rl`.
5. **Alternate resolvers** — `-r` with a trusted or internal list; avoid poisoned/open resolvers for authoritative work.
6. **Disable stream assumptions** — If using `-stream`, remember wildcard/resume are off.

## Wildcard / synthetic answers

1. Spot identical A answers across random labels.
2. Enable `-auto-wildcard` or pin `-wd <domain>` (JSON recommended; exclusive with auto).
3. Tune `-wt` (default 5).
4. Re-check survivors with a second resolver set before emitting host nuggets.
5. Do not treat every bruteforce hit as a real host without wildcard controls.

## SERVFAIL / REFUSED / flaky resolvers

1. Capture `-rcode` filters when isolating NOERROR-only corpus rows.
2. Rotate `-r`; do not conclude NXDOMAIN from one resolver failure.
3. Lower `-t` and `-rl` under rate pressure.
4. Record **error** scenarios separately from clean misses.

## Maximizing enrichment without noise

| Pass | Flags | Why |
|------|-------|-----|
| 1 — Liveness | `-a -aaaa -json` | Cheap validation |
| 2 — Alias | `-cname` (+ `-cdn`) | SaaS/CDN clusters |
| 3 — Mail | `-mx -txt` | SPF / exchangers |
| 4 — Authority | `-ns -soa` | DNS hosting |
| 5 — Broad | `-all` / `-recon` | Only high-value hosts |

Prefer staged passes over blanket `-all` on huge lists.

## Bruteforce tactics

1. Start with a small high-signal wordlist; expand only if yield is thin.
2. Keep `-auto-wildcard` on during brute (not with `-stream`).
3. Immediately re-validate hits with enrichment flags before httpx/naabu.
4. Deduplicate against passive subfinder results.

## Maximize downstream value

| dnsx output | Next tool |
|-------------|-----------|
| `host` + `a`/`aaaa` | httpx, naabu |
| `cname` clusters | Targeted nuclei tags / takeover checks (authorized) |
| `mx` / SPF TXT | Email security modules |
| `ns` / SOA | Provider / zone follow-ups |
| `ptr` names | Fresh dnsx A/AAAA → httpx |

## Rate and OPSEC

1. Default `-t 100` may be aggressive on shared resolvers — tune down for long runs.
2. Prefer scoped lists over internet-wide brute.
3. `-proxy` is available for socks5 when required by engagement rules.
4. `-duc` in CI to avoid update-check noise.
