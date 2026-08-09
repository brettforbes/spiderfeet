# uncover Tactics and Workflows

## Where uncover sits

```
org / product / SSL dork  →  uncover (-json)  →  httpx / naabu / nuclei
IP/CIDR inventory         →  uncover -e shodan-idb|driftnet  →  httpx / naabu
subfinder hostnames       →  (optional) uncover host/ssl pivots  →  dnsx / httpx
```

uncover expands **indexed** exposure. It does not replace active scanning or DNS enumeration.

## Workflow A — Focused single-provider search

1. Configure one engine’s API key (`-pc` / env).
2. Write a narrow dork (`org:`, `ssl:`, `product:` + `port:`, hostname).
3. Run: `uncover -q '…' -e shodan -json -silent -l 100 -o phase.jsonl`
4. Map nuggets; pick top `ip:port` for httpx/naabu validation.

## Workflow B — Multi-provider correlation

1. Express the same intent in **native** syntax per engine (`-shodan`, `-censys`, `-fofa`, …).
2. Run once with multiple per-engine flags (or sequential `-e` runs).
3. Merge JSONL on `(ip, port)`; tag `source` set.
4. Prefer cross-engine hits for deeper validation budget.

## Workflow C — Keyless IP / CIDR enrich

1. Feed IP or CIDR on stdin / `-q`.
2. Default engine becomes **`shodan-idb`** (no key), or set `-e driftnet` when Driftnet keys/policy allow.
3. Capture `-json`; treat ports as **index leads**, then confirm with naabu if scope requires active truth.

```bash
echo '51.83.59.99/24' | uncover -json -silent -o idb.jsonl
echo '8.8.8.8/20' | uncover -e driftnet -json -silent -o driftnet.jsonl
```

## Workflow D — Awesome search queries

1. Use `-asq <pack>` (e.g. `jira`) for curated exposure hunts.
2. Still add `-json -silent` and scope filters where the pack is too broad.
3. Validate before claiming product exposure.

## Workflow E — Pipeline into PD tools

```bash
uncover -q 'title:"GitLab"' -e shodan -silent | httpx -silent -json
uncover -q 'org:"Example Inc."' -f ip -silent | naabu -top-ports 100 -json -silent
uncover -q 'org:"Example Inc."' -silent | httpx -silent | nuclei -silent -jsonl
```

For SpiderFeet formal examination, prefer **JSONL files** over text pipes so harvest can build `records[]`.

## Tactics when yield is wrong

| Symptom | Adaptation |
|---------|------------|
| Zero results | Check keys; fix provider-native syntax; try another `-e`; raise `-timeout` / `-retry` |
| Huge noisy set | Add org/ssl/hostname/port constraints; lower `-l`; split queries |
| Rate limit / 429 | `-rl` / `-rlm`; multiple keys in provider-config; backoff; switch engine |
| CDN / shared IP confusion | Do not attribute org solely from anycast IP; require host/ssl corroboration |
| Auth failures mid multi-engine | Keep successful engines’ JSONL; document failed `source` as blocked scenario |
| Need richer vendor fields | `-raw` for exploration only; normalized `-json` remains exam source |

## Semantic outcome matrix (profiling gate)

Plan formal scenarios covering at least:

| Outcome class | Suggested approach |
|---------------|--------------------|
| Rich host/port rows | Permissive org/product dork + paid engine + `-json` |
| Sparse / clean miss | Obscure org or over-constrained dork |
| Keyless IP enrich | `shodan-idb` on lab/public IP |
| Multi-engine merge | Same intent, two+ engines |
| Auth / missing key | Engine without credentials |
| Invalid flag combo | Document `-silent`+`-v` fatal (error fixture) |
| Field-shaped text | Exploration only (`-f`); not a paired exam when `-json` exists |

## Sequencing rules

1. **Prove keys** with a tiny `-l 5` JSON run before large pulls.
2. **JSON always** for corpus: `-json -o phase.jsonl`.
3. **Validate** high-value ports before nuclei severity claims.
4. **Diff** scheduled runs for net-new `ip:port` exposure monitoring.
