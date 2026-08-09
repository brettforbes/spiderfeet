# uncover Zero to Hero — Provider Search, JSONL, and Nuggets

From install to orchestrated recon with **`uncover -json`**, nugget mapping, and pipelines to **httpx**, **naabu**, and **nuclei**.

Skill reference: `.cursor/skills/uncover/SKILL.md`

**Binary (this repo):** `C:\projects\spiderfeet\.tools\uncover\uncover.exe` — **v1.2.1** (help captured **2026-08-10**).

## What uncover does

uncover is ProjectDiscovery’s **Go wrapper around internet search-engine APIs**. It turns provider dorks (or IP/CIDR lookups) into normalized host/port hits for automation pipelines.

uncover does **not**:

- Actively SYN/CONNECT scan ports (use **naabu** / **nmap**)
- Enumerate subdomains passively from certificate transparency alone (use **subfinder**)
- Probe HTTP content (use **httpx**)
- Run vulnerability templates (use **nuclei**)

---

## Level 0 — Install and verify

```bash
go install -v github.com/projectdiscovery/uncover/cmd/uncover@latest
uncover -version
```

Or: https://github.com/projectdiscovery/uncover/releases

This workspace:

```powershell
& "C:\projects\spiderfeet\.tools\uncover\uncover.exe" -version
```

Expected (capture **2026-08-10**): `Current Version: v1.2.1`

---

## Level 1 — Provider keys

Most engines need API credentials before they return data. Configure `%APPDATA%\uncover\provider-config.yaml` (see `-pc`) or environment variables documented in the [README](https://github.com/projectdiscovery/uncover/blob/main/README.md).

**Exception:** `shodan-idb` (Shodan InternetDB) works **without** a key and is the default engine when input is an **IP/CIDR**.

---

## Level 2 — First keyless IP enrich

```bash
uncover -q '1.1.1.1' -e shodan-idb -silent
```

Default field format is `ip:port`.

---

## Level 3 — JSONL for automation (preferred)

```bash
uncover -q '1.1.1.1' -e shodan-idb -json -silent -o uncover.jsonl
```

Example line:

```json
{"timestamp":1786295459,"source":"shodan-idb","ip":"1.1.1.1","port":443,"host":"example.com","url":""}
```

**Always prefer `-json` for SpiderFeet** — parse line by line into harvest `records[]`.

Fields: `timestamp`, `source`, `ip`, `port`, `host`, `url`.

---

## Level 4 — Search dorks (Shodan default)

With a Shodan API key configured:

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent -l 50
echo 'ssl:"Example Org"' | uncover -json -silent
uncover -q dorks.txt -e shodan -json -silent
```

Query filters are **those supported by the selected engine** only.

---

## Level 5 — Multi-engine and per-engine syntax

Same intent, different native filters:

```bash
uncover -q jira -e shodan,censys,fofa -json -silent

uncover -shodan 'http.component:"Atlassian Jira"' \
  -censys 'services.software.product=`Jira`' \
  -fofa 'app="ATLASSIAN-JIRA"' \
  -json -silent
```

Engines exposed by this binary’s `-e` help include: `shodan`, `shodan-idb`, `fofa`, `censys`, `quake`, `hunter`, `zoomeye`, `netlas`, `publicwww`, `criminalip`, `hunterhow`, `google`, `odin`, `binaryedge`, `onyphe`, `driftnet`, `greynoise`, `daydaymap`, `nerdydata`.

---

## Level 6 — Field shaping for pipes

Text pipelines (not the graph source when JSON exists):

```bash
uncover -q jira -f host -silent
uncover -q jira -f https://ip:port/version -silent
uncover -q 'org:"Example Inc."' -f ip -silent | naabu -json -silent
```

---

## Level 7 — Awesome search queries

```bash
uncover -asq jira -json -silent
```

---

## Level 8 — Pipelines

```bash
uncover -q 'title:"GitLab"' -e shodan -silent | httpx -silent -json
uncover -q 'org:"Example Inc."' -silent | httpx -silent | nuclei -silent -jsonl
echo '51.83.59.99/24' | uncover -e shodan-idb -silent | httpx -silent
```

---

## Level 9 — Nugget mapping (SpiderFeet)

From each JSONL row:

| Field | Nugget |
|-------|--------|
| `ip` | `IPV4_ADDRESS` / `IPV6_ADDRESS` via `classify_ip` |
| `host` | `INTERNET_NAME` when non-empty |
| `port` | `TCP_PORT_OPEN` (provider-reported) |
| `source` | Provenance metadata |

Treat results as **leads**. Confirm with httpx/naabu before severity claims. Details: `.cursor/skills/uncover/references/nugget-mapping.md`.

---

## Level 10 — Rate limits, retries, proxies

```bash
uncover -q jira -e shodan -json -silent -timeout 60 -retry 3 -rl 1
uncover -q jira -e shodan -json -silent -proxy http://127.0.0.1:8080
```

Default result **limit is 100** (`-l`).

---

## Pitfalls

- Missing API keys → empty or error output for paid engines.
- `-silent` and `-v` together → fatal exit.
- Do not invent flags (no `-csv` on **v1.2.1**).
- Do not reuse Shodan syntax on FOFA/Censys unchanged.
- JSONL is not a JSON array — parse line by line.
- Formal examination: structured JSON only; derive Text from records.

---

## Next reading

| Doc | Role |
|-----|------|
| `.docs/docs-for-cli-tools/uncover-CLI-Options.md` | Full flag reference + captured help |
| `.cursor/skills/uncover/SKILL.md` | Agent workflow |
| `.cursor/skills/uncover/references/tactics.md` | Scenario tactics |
