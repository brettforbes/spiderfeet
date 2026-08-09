# Julius Tactics — Shadow AI and Adaptive Probing

## Shadow AI / enterprise discovery

Goal: find **unsanctioned LLM endpoints** on corporate attack surface.

1. **Passive asset list** — subdomains, internal DNS, cloud IPs from Pius/uncover.
2. **Port sweep** — Naabu on LLM port shortlist (see workflows-and-phases.md).
3. **URL construction** — `https://{host}:{port}` for each open port; include `:443` / `:8443` with bare hostname.
4. **Julius JSONL** — `julius probe -f urls.txt -o jsonl > julius.jsonl`; flag `specificity >= 75` as high-confidence shadow AI.
5. **Model inventory** — rows with `models[]` for data-governance reporting.
6. **Augustus handoff** — `--augustus` for authorized prompt-injection / safety assessment on confirmed endpoints.

## Chain: Naabu → Julius

```bash
naabu -host corp.example.com -p 11434,8000,8080,7860,4000,3000 -json -silent | \
  jq -r '"https://" + (if .host then .host else .ip end) + ":" + (.port|tostring)' | \
  julius probe - -o jsonl
```

Windows PowerShell variant:

```powershell
naabu -host corp.example.com -p 11434,8000,8080 -json -silent |
  ForEach-Object { $_ | ConvertFrom-Json } |
  ForEach-Object { "https://$($_.ip):$($_.port)" } |
  & "C:\projects\spiderfeet\.tools\julius\julius.exe" probe - -o jsonl
```

## Chain: Nmap → Julius

```bash
nmap -p 11434,8000,8080,7860,4000 --open -oG - 10.0.0.0/24 | grep open |
  awk '{print "https://" $2 ":11434"}' | julius probe - -o jsonl
```

Prefer one URL per **open port** (do not hardcode a single port for every host).

## Hostile / filtered environments

| Defense | Tactic |
|---------|--------|
| WAF on `/v1/*` paths | `-v` to see which requests fail; try `--base-paths` |
| Rate limiting | Lower `-c`; increase `-t` |
| TLS inspection / custom CA | `--ca-cert` or (lab only) `--insecure` |
| IP allowlists | Run from approved scanner egress |
| Auth-required endpoints | Julius is unauthenticated; auth gaps = manual follow-up |
| CDN fronting | Probe origin IP if known; CDN may mask signatures |
| Path-prefixed reverse proxies | `--base-paths /api,/proxy` |

## Specificity-based triage

| Specificity | Action |
|-------------|--------|
| 100 (e.g. Ollama) | Emit nuggets immediately; optional model enumeration |
| 75–95 | High confidence; document category |
| 50 | Medium — corroborate with second tool or manual check |
| 1 (`openai-compatible`) | Label "OpenAI-compatible API surface"; do not claim product |

## When to stop escalating

- Investigation goal satisfied (inventory of LLM services on scope).
- All targets timeout after `-t 30` — network unreachable or blocked.
- Legal/scope boundary — stop at authorized CIDRs only.

## Negative / clean-miss scenarios

```bash
julius probe -o json https://example.com
julius probe -o jsonl -f non_ai_hosts.txt
```

Expect `[]` or JSONL with no match lines (or only errors). Verdict: `clean_miss` when no `service` matches.
