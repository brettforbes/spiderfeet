# Nerva CLI Options

**Synopsis:**

```
nerva [flags]
```

Targets are **`host:port`** or **`ip:port`**. Nerva assumes ports are already open.

Install: https://github.com/praetorian-inc/nerva/releases or `go install github.com/praetorian-inc/nerva/cmd/nerva@latest`

---

## Target specification

### `--targets` / `-t`

Single target or comma-separated list.

```bash
nerva -t example.com:22
nerva -t example.com:22,example.com:80,example.com:443
nerva --targets 192.168.1.10:22,192.168.1.10:3306 --json
```

### `--list` / `-l`

File with one `host:port` per line.

```
example.com:22
example.com:80
192.168.1.50:443
```

```bash
nerva -l targets.txt --json
```

### Stdin

Nerva accepts `host:port` lines on stdin when no `-t`/`-l` targets are given (common in pipes).

```bash
cat targets.txt | nerva --json
naabu -host example.com -silent | nerva --json
echo "10.0.0.1:22" | nerva --json
```

---

## `--output` / `-o`

Write results to file instead of stdout.

```bash
nerva -l targets.txt --json -o results.jsonl
nerva -l targets.txt --csv -o results.csv
```

Default: human-readable or selected format to **stdout**.

---

## `--json`

Emit **JSON Lines** (one JSON object per fingerprinted service).

```bash
nerva -t example.com:22 --json
```

Example record:

```json
{"host":"example.com","ip":"93.184.216.34","port":22,"protocol":"ssh","transport":"tcp","metadata":{"banner":"SSH-2.0-OpenSSH_8.9p1"}}
```

**Required for SpiderFeet parsers** — do not parse default `protocol://host:port` text.

---

## `--csv`

Comma-separated values with header row.

```bash
nerva -t example.com:22 --csv
```

Typical columns: `host`, `ip`, `port`, `protocol`, `transport`, `tls`

```csv
host,ip,port,protocol,transport,tls
example.com,93.184.216.34,22,ssh,tcp,false
```

---

## `--fast` / `-f`

Fast mode — only run the **default-port plugin** for each protocol class; skips exhaustive cross-protocol probing.

```bash
nerva -l ten_thousand_targets.txt --fast --json
```

**Trade-off:** faster, but may miss services on non-standard ports.

---

## `--udp` / `-U`

Enable **UDP** fingerprint plugins (DNS, SNMP, NTP, DHCP, etc.).

```bash
sudo nerva -t example.com:53 -U --json
sudo nerva -l udp_targets.txt -U --json -o udp.jsonl
```

May require elevated privileges for raw UDP sockets.

---

## `--sctp` / `-S`

Enable **SCTP** plugins (e.g. Diameter). **Linux only.**

```bash
nerva -t mme.telecom.local:3868 -S --json
```

---

## `--timeout` / `-w`

Per-probe timeout in **milliseconds** (default `2000`).

```bash
nerva -t slow-server.example.com:8080 -w 5000 --json
nerva -l targets.txt -w 10000 --json
```

Increase for high-latency links or slow handshakes.

---

## `--verbose` / `-v`

Verbose diagnostic messages to **stderr** (does not change JSON stdout structure).

```bash
nerva -l targets.txt --json -v 2>nerva.log
```

---

## `--help` / `-h`

Show usage and exit.

```bash
nerva -h
```

---

## Output format comparison

| Flag | Format | SpiderFeet use |
|------|--------|----------------|
| *(none)* | `ssh://host:22` text | Operator only |
| `--json` | JSON Lines | **Primary parser input** |
| `--csv` | CSV with header | Spreadsheet / alternate ETL |

---

## Flag combinations (recipes)

| Scenario | Command |
|----------|---------|
| Standard module run | `nerva -l targets.txt --json -o out.jsonl` |
| Naabu pipe | `naabu -host TARGET -silent \| nerva --json` |
| Large scan, speed | `nerva -l targets.txt --fast --json` |
| DNS fingerprint | `sudo nerva -t 10.0.0.1:53 -U --json` |
| Slow services | `nerva -l targets.txt -w 8000 --json` |
| Debug failures | `nerva -t host:port --json -v` |

---

## Environment and privileges

| Transport | Privilege notes |
|-----------|-----------------|
| TCP | Usually unprivileged |
| UDP | Often requires root |
| SCTP | Linux + often root |

---

## Version check

```bash
nerva -h
# or
nerva --help
```

Wiki documents 54 plugins; blog mentions 120+ protocol checks via multi-probe plugins — treat `protocol` field as canonical identity.
