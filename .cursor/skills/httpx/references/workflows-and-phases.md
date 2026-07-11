# httpx Workflows and Phases

## Phase model

| Phase | Tool | Output |
|-------|------|--------|
| A — Names | subfinder, amass | Hostname list |
| B — DNS validate | dnsx | Resolvable FQDNs + IPs |
| C — **HTTP probe** | **httpx** | Live URLs + fingerprint JSONL |
| D — Ports | naabu, nmap | Open TCP ports |
| E — **HTTP on ports** | **httpx** (again) | URLs on 8080/8443/etc. |
| F — Vuln / depth | nuclei | Findings JSONL |

httpx may run **twice**: after DNS (standard 80/443) and after port scan (non-standard web ports).

## Workflow 1 — Classic recon chain

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa | tee live.txt
cat live.txt | httpx -title -tech-detect -status-code -json -silent -o web.jsonl
cat web.jsonl | jq -r '.url' | nuclei -silent -jsonl -tags cve
```

## Workflow 2 — Ports then web

```bash
naabu -host example.com -top-ports 1000 -json -silent -o ports.jsonl
# Map open web ports to URLs, then:
httpx -l web_targets.txt -json -silent -o web.jsonl
```

## Workflow 3 — Corpus capture

```bash
httpx -l hosts.txt -status-code -title -tech-detect -server -cdn -ip \
  -json -include-chain -o examination/web_probe.jsonl
```

Harvest → `httpx_probe_v1` bundle with `records[]`.

## Workflow 4 — Matcher-filtered nuclei feed

```bash
httpx -l hosts.txt -match-code 200,301,302,401,403 -json -silent \
  | nuclei -silent -jsonl -severity critical,high
```

## Workflow 5 — Path enumeration (isolated)

```bash
httpx -l base_urls.txt -path /api,/admin,/swagger,/v1 -sc -json -o paths.jsonl
```

## Workflow 6 — Redirect matrix

```bash
httpx -l hosts.txt -follow-redirects -json -include-chain -o redirects.jsonl
```

## Workflow 7 — ASN / CIDR sweep

```bash
echo AS15169 | httpx -json -silent
echo 10.10.0.0/24 | httpx -json -silent -o cidr_web.jsonl
```

## SpiderFeet seed mapping

| Seed | Typical httpx input |
|------|---------------------|
| `DOMAIN_NAME` | After subfinder: hostnames |
| `INTERNET_NAME` | `httpx -u https://SEED` |
| `IP_ADDRESS` | `httpx -u http://SEED` or IP URL |
| `TCP_PORT_OPEN` | Build `http://ip:port` list from naabu JSON |

## Ontology placement

httpx results attach to **qualified `HOST`** sub-graph: `APPLICATIONS`, `LINKED_URL_INTERNAL`, `WEBSERVER_*` descriptors — see `_Current_Ontology.md`.

## Phase decisions

| Observation | Next step |
|-------------|-----------|
| No URLs from big host list | dnsx validation; `-no-fallback`; check ports |
| Only CDN tech detected | Origin hunt or accept edge-only evidence |
| Many 301/302 | `-include-chain`; nuclei on final URLs |
| Open 8080 from naabu | Second httpx pass with `-p http:8080` |
