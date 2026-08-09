# mapcidr CLI Options

Invocation: **`mapcidr`**. SpiderFeet formal examination defaults to **line output + `-silent`**, then parse into a JSON bundle (this binary has **no** JSON flag).

```bash
mapcidr -cidr 10.0.0.0/30 -silent
echo "10.0.0.0/30" | mapcidr -silent
mapcidr -cl cidrs.txt -silent -o expanded.txt
```

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe` |
| Version | **v1.1.97** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_mapcidr_help/help_h.txt`, `help_long.txt`, `version.txt` |

> Flags below are from live `-h` / `-version` only — **do not invent options**.  
> `help_h.txt` and `help_long.txt` are identical for this capture.  
> There is **no** `-json` / `-j` / `-oJ`. Prefer structured harvest by parsing `-silent` lines.

## Captured help

Live help from `.tools/mapcidr/mapcidr.exe` on **2026-08-10**:

```text
mapCIDR is developed to ease load distribution for mass scanning operations, it can be used both as a library and as independent CLI tool.

Usage:
  C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe [flags]

Flags:
CONFIG:
   -auth  configure projectdiscovery cloud (pdcp) api key (default true)

INPUT:
   -cl, -cidr string[]  CIDR/IP/File containing list of CIDR/IP to process

PROCESS:
   -sbc int                  Slice CIDRs by given CIDR count
   -sbh int                  Slice CIDRs by given HOST count
   -a, -aggregate            Aggregate IPs/CIDRs into minimum subnet
   -aa, -aggregate-approx    Aggregate sparse IPs/CIDRs into minimum approximated subnet
   -c, -count                Count number of IPs in given CIDR
   -t4, -to-ipv4             Convert IPs to IPv4 format
   -t6, -to-ipv6             Convert IPs to IPv6 format
   -ip-format, -if string[]  IP formats (0,1,2,3,4,5,6,7,8,9,10,11)
   -zpn, -zero-pad-n int     number of padded zero to use (default 3)
   -zpp, -zero-pad-permute   enable permutations from 0 to zero-pad-n for each octets

FILTER:
   -f4, -filter-ipv4         Filter IPv4 IPs from input
   -f6, -filter-ipv6         Filter IPv6 IPs from input
   -skip-base                Skip base IPs (ending in .0) in output
   -skip-broadcast           Skip broadcast IPs (ending in .255) in output
   -mi, -match-ip string[]   IP/CIDR/FILE containing list of IP/CIDR to match (comma-separated, file input)
   -fi, -filter-ip string[]  IP/CIDR/FILE containing list of IP/CIDR to filter (comma-separated, file input)

MISCELLANEOUS:
   -s, -sort                  Sort input IPs in ascending order
   -sr, -sort-reverse         Sort input IPs in descending order
   -si, -shuffle-ip           Shuffle Input IPs in random order
   -sp, -shuffle-port string  Shuffle Input IP:Port in random order

UPDATE:
   -up, -update                 update mapcidr to latest version
   -duc, -disable-update-check  disable automatic mapcidr update check

OUTPUT:
   -verbose            Verbose mode
   -o, -output string  File to write output to
   -silent             Silent mode
   -version            Show version of the project
```

### Version banner (`mapcidr -version`)

```text
[INF] Current Version: v1.1.97
```

(Full ANSI banner retained in `.tmp_mapcidr_help/version.txt`.)

### Re-capture

```powershell
$out = "C:\projects\spiderfeet\.tmp_mapcidr_help"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$mc = "C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe"
& $mc -h 2>&1 | Set-Content "$out\help_h.txt"
& $mc -h 2>&1 | Set-Content "$out\help_long.txt"
& $mc -version 2>&1 | Set-Content "$out\version.txt"
```

## Synopsis

```
mapcidr -cidr <CIDR|IP|file> [flags]
mapcidr -cl <CIDR|IP|file> [flags]
echo <CIDR|range|IP> | mapcidr [flags]
```

Stdin is supported (pipe). Primary input flag is **`-cl` / `-cidr`** — not `-l`.

## Options reference

| Flag | Short/alt | Type | Description (from help) |
|------|-----------|------|-------------------------|
| `-auth` | | bool | configure projectdiscovery cloud (pdcp) api key (default true) |
| `-cidr` | `-cl` | string[] | CIDR/IP/File containing list of CIDR/IP to process |
| `-sbc` | | int | Slice CIDRs by given CIDR count |
| `-sbh` | | int | Slice CIDRs by given HOST count |
| `-aggregate` | `-a` | bool | Aggregate IPs/CIDRs into minimum subnet |
| `-aggregate-approx` | `-aa` | bool | Aggregate sparse IPs/CIDRs into minimum approximated subnet |
| `-count` | `-c` | bool | Count number of IPs in given CIDR |
| `-to-ipv4` | `-t4` | bool | Convert IPs to IPv4 format |
| `-to-ipv6` | `-t6` | bool | Convert IPs to IPv6 format |
| `-ip-format` | `-if` | string[] | IP formats (0–11); `0` shows all |
| `-zero-pad-n` | `-zpn` | int | number of padded zero to use (default 3) |
| `-zero-pad-permute` | `-zpp` | bool | enable permutations from 0 to zero-pad-n for each octets |
| `-filter-ipv4` | `-f4` | bool | Filter IPv4 IPs from input |
| `-filter-ipv6` | `-f6` | bool | Filter IPv6 IPs from input |
| `-skip-base` | | bool | Skip base IPs (ending in .0) in output |
| `-skip-broadcast` | | bool | Skip broadcast IPs (ending in .255) in output |
| `-match-ip` | `-mi` | string[] | IP/CIDR/FILE to match |
| `-filter-ip` | `-fi` | string[] | IP/CIDR/FILE to filter (exclude) |
| `-sort` | `-s` | bool | Sort ascending |
| `-sort-reverse` | `-sr` | bool | Sort descending |
| `-shuffle-ip` | `-si` | bool | Shuffle IPs |
| `-shuffle-port` | `-sp` | string | Shuffle IP:Port |
| `-update` | `-up` | bool | update mapcidr |
| `-disable-update-check` | `-duc` | bool | disable automatic update check |
| `-verbose` | | bool | Verbose mode |
| `-output` | `-o` | string | File to write output to |
| `-silent` | | bool | Silent mode |
| `-version` | | bool | Show version |

### Observed notes (2026-08-10 local probes)

- **`-f4` / `-f6`:** on a mixed IPv4+IPv6 stdin sample, `-f4` kept IPv4 only and `-f6` kept IPv6 only. Always spot-check before large runs.
- **`-sp`:** `echo 1.1.1.1 \| mapcidr -sp 80 -silent` → `1.1.1.1:80`. Bare `ip:port` lines without `-sp` can fail as invalid CIDR.
- **ASN (`ASnnnn`) stdin:** without pdcp key → `[FTL] unauthorized: 401` (cloud feature).
- Perfect slice splits prefer power-of-two counts/hosts (upstream README note).

## Option classes and examples

### INPUT

```bash
mapcidr -cidr 10.0.0.0/24 -silent
mapcidr -cl cidrs.txt -silent
echo "192.168.0.0-192.168.0.5" | mapcidr -silent
```

### PROCESS — slice / aggregate / count / convert / formats

```bash
mapcidr -cidr 10.0.0.0/24 -sbc 4 -silent
mapcidr -cidr 10.0.0.0/24 -sbh 64 -silent
mapcidr -cl cidrs.txt -a -silent
printf "1.1.1.1\n1.1.1.16\n1.1.1.31\n" | mapcidr -aa -silent
echo "10.0.0.0/24" | mapcidr -c -silent
mapcidr -cl ips.txt -t6 -silent
echo "127.0.1.0" | mapcidr -if 0 -silent
```

### FILTER

```bash
mapcidr -cidr 10.0.0.0/29 -skip-base -skip-broadcast -silent
mapcidr -cidr 192.168.1.0/24 -mi 192.168.1.1,192.168.1.2 -silent
mapcidr -cidr 192.168.1.224/28 -fi 192.168.1.233,192.168.1.234 -silent
printf "1.1.1.1\n2001:db8::1\n" | mapcidr -f4 -silent
```

### MISCELLANEOUS / OUTPUT

```bash
printf "10.0.0.3\n10.0.0.1\n" | mapcidr -s -silent
echo "1.1.1.1" | mapcidr -sp 80,443 -silent
mapcidr -cidr 10.0.0.0/30 -silent -o hosts.txt
mapcidr -cidr 10.0.0.0/30 -verbose
```

## Not present on this binary

Do **not** document or use:

- `-json` / `-j` / `-oJ` / NDJSON mode
- `-l` / `-list` / `-il` as input aliases (not in help)
- any invented XML/YAML exporters
