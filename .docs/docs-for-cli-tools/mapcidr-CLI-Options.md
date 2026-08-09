# mapcidr CLI Options

Operator reference for **ProjectDiscovery mapcidr**. This binary has **no JSON flag** — prefer **`-silent` line output**, then parse into a SpiderFeet JSON `records[]` bundle.

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe` |
| Version | **v1.1.97** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_mapcidr_help/help_h.txt`, `help_long.txt`, `version.txt` |

> Flags below are from live `-h` / `-version` only — **do not invent options**.  
> `help_h.txt` and `help_long.txt` are identical for this capture.

Skill: `.cursor/skills/mapcidr/SKILL.md`

---

## SpiderFeet preferred commands

```bash
mapcidr -cidr 10.0.0.0/30 -silent
echo "10.0.0.0/30" | mapcidr -silent
mapcidr -cl cidrs.txt -silent -o expanded.txt
mapcidr -cidr 10.0.0.0/16 -sbh 4096 -silent
mapcidr -cl ips.txt -a -silent
echo "10.0.0.0/24" | mapcidr -c -silent
```

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe` on **2026-08-10**. Each block is the full stdout of the listed command (ANSI sequences retained where present in the version capture file).

### Version (`mapcidr -version`)

```text

                   ____________  ___    
  __ _  ___ ____  / ___/  _/ _ \/ _ \   
 /  ' \/ _ '/ _ \/ /___/ // // / , _/   
/_/_/_/\_,_/ .__/\___/___/____/_/|_|
          /_/                                                     	 

		projectdiscovery.io

[[34mINF[0m] Current Version: v1.1.97
```

### Root help (`mapcidr -h`)

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

---

## Options by class

### CONFIG

| Flag | Description |
|------|-------------|
| `-auth` | configure projectdiscovery cloud (pdcp) api key (default true) |

Needed for cloud-backed features such as ASN expansion (`ASnnnn` input). Without a key, ASN runs return `unauthorized: 401`.

### INPUT

| Flag | Description |
|------|-------------|
| `-cl`, `-cidr` | CIDR/IP/File containing list of CIDR/IP to process |

Also accepts **stdin** pipes. Ranges like `192.168.0.0-192.168.0.5` work on stdin (README + local probe).

**Not in help:** `-l`, `-il`, `-list`.

### PROCESS

| Flag | Description |
|------|-------------|
| `-sbc` | Slice CIDRs by given CIDR count |
| `-sbh` | Slice CIDRs by given HOST count |
| `-a`, `-aggregate` | Aggregate IPs/CIDRs into minimum subnet |
| `-aa`, `-aggregate-approx` | Aggregate sparse IPs/CIDRs into minimum approximated subnet |
| `-c`, `-count` | Count number of IPs in given CIDR |
| `-t4`, `-to-ipv4` | Convert IPs to IPv4 format |
| `-t6`, `-to-ipv6` | Convert IPs to IPv6 format |
| `-ip-format`, `-if` | IP formats (0–11) |
| `-zpn`, `-zero-pad-n` | padded zero count (default 3) |
| `-zpp`, `-zero-pad-permute` | permute zero-pad widths |

### FILTER

| Flag | Description |
|------|-------------|
| `-f4`, `-filter-ipv4` | Filter IPv4 IPs from input |
| `-f6`, `-filter-ipv6` | Filter IPv6 IPs from input |
| `-skip-base` | Skip base IPs (ending in .0) |
| `-skip-broadcast` | Skip broadcast IPs (ending in .255) |
| `-mi`, `-match-ip` | Match allow list |
| `-fi`, `-filter-ip` | Filter/exclude list |

Local probe note (2026-08-10): on mixed stdin, `-f4` kept IPv4 only; `-f6` kept IPv6 only. Spot-check before large jobs.

### MISCELLANEOUS / UPDATE / OUTPUT

| Flag | Description |
|------|-------------|
| `-s`, `-sort` | ascending sort |
| `-sr`, `-sort-reverse` | descending sort |
| `-si`, `-shuffle-ip` | shuffle IPs |
| `-sp`, `-shuffle-port` | shuffle IP:Port |
| `-up`, `-update` | update mapcidr |
| `-duc`, `-disable-update-check` | disable update check |
| `-verbose` | verbose |
| `-o`, `-output` | write to file |
| `-silent` | silent |
| `-version` | show version |

---

## Structured output note

mapcidr **does not** expose `-json` / `-j` / `-oJ` on v1.1.97. For SpiderFeet corpus work:

1. Run with `-silent`.
2. Parse one value per line into a single JSON bundle (`schema: mapcidr_lines_v1`, `records[]`).
3. Derive the Text pane from `records`.
4. Build graph + narrative from the structured bundle.

See `.cursor/skills/mapcidr/references/output-and-parsing.md`.
