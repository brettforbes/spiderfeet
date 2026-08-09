---
name: mapcidr
description: Expand and normalize CIDRs/ranges with mapcidr, then convert results into SpiderFeet netblock and host graph artifacts. Trigger on mapcidr, CIDR expansion, IP-range splitting, netblock preprocessing, or host-target generation for recon pipelines.
---

# mapcidr — CIDR Expansion, Slicing, and Aggregation

## Purpose

Use when you must **expand, slice, aggregate, count, filter, or reformat** CIDRs / IP ranges / IP lists into clean target sets for mass scanning, then convert line output into SpiderFeet **netblock** and **address** nuggets — especially before **naabu**, **nmap**, **httpx**, or **dnsx** host/port work.

**Binary (this host):** `C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe`  
**Version:** **v1.1.97** (`mapcidr -version`)  
**Help capture:** **2026-08-10** (`.tmp_mapcidr_help/`)

**No JSON / NDJSON flag** on this binary. Output is one IP, CIDR, IP:port, or count per line. For SpiderFeet formal examination, capture `-silent` lines and **parse into a single JSON bundle** (`records[]`) — do not invent a `-json` option.

## Step-by-Step Instructions

1. **Confirm authorized netblock scope** — only expand ranges you are allowed to scan or process.
2. **Validate tooling** — `mapcidr -version` and `mapcidr -h` (exact text in `references/cli-options.md` and `.docs/docs-for-cli-tools/mapcidr-CLI-Options.md`).
3. **Prepare input** — CIDR, IP, IP range (`a.b.c.d-w.x.y.z`), or file of the same; pass via `-cl` / `-cidr` or stdin.
4. **Choose process mode:**
   - default = expand to hosts
   - `-sbc N` / `-sbh N` = slice for load distribution
   - `-a` / `-aa` = aggregate to minimum (approx) subnets
   - `-c` = count hosts (prints a number, not an IP list)
5. **Apply filters** when needed — `-skip-base`, `-skip-broadcast`, `-mi` / `-fi`, `-f4` / `-f6` (see decision rules; verify family keep/drop with a tiny sample).
6. **Run with `-silent`** for clean one-value-per-line stdout (banner suppressed).
7. **Optionally write** `-o file` and/or sort/shuffle (`-s`, `-sr`, `-si`, `-sp`).
8. **Parse lines → structured bundle** — validate IP/CIDR/IP:port; attach provenance (source CIDR, command, timestamp).
9. **Map nuggets** — input CIDR → `NETBLOCK_OWNER` / `NETBLOCKV6_OWNER`; hosts via `classify_ip` → `IPV4_ADDRESS` / `IPV6_ADDRESS` / `INTERNAL_IP_ADDRESS`; edges use `contains` (see `references/nugget-mapping.md`).
10. **Feed downstream** — pipe or file into naabu/nmap/httpx; keep sliced CIDRs when scanners prefer netblocks over huge IP lists.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Use `-silent`; parse lines into a JSON `records[]` bundle (no native JSON flag) |
| Netblock too large for one scan | Slice with `-sbc` or `-sbh` before downstream tools |
| Overlapping CIDRs / duplicate hosts | Expand once, dedupe lines (`sort -u` or set), keep provenance |
| Downstream is IPv4-only | Prefer `-f4` after confirming keep-IPv4 behavior on a sample |
| Need IPv6-only set | Prefer `-f6` after confirming keep-IPv6 behavior on a sample |
| Want fewer useless edge hosts | `-skip-base` and/or `-skip-broadcast` (IPv4 `.0` / `.255` style skips) |
| Need minimum covering subnets | `-a` (exact aggregate) or `-aa` (approx, sparse IPv4) |
| Only need size of space | `-c -silent` → integer count |
| ASN seed (`ASnnnn`) | Requires ProjectDiscovery cloud key (`-auth` / pdcp); expect `401 unauthorized` without it |
| Need IP:port fan-out for scanners | `-sp <ports>` on IP input (produces `ip:port` lines) |
| Human exploration | Omit `-silent` briefly; formal capture still uses silent lines |

## Guardrails & Pitfalls

- **Authorization** — expansion is offline math, but outputs often drive active scans; keep scope explicit.
- **Do not invent flags** — only options from Captured help (2026-08-10). There is **no** `-json`, **no** `-l` (use `-cl` / `-cidr`), and **no** `-il` in this binary’s help.
- **Do not explode huge ranges** without slice/count first (`-c`, `-sbc`, `-sbh`).
- **Preserve provenance** — every host line should remember source CIDR/range.
- **Output order is not priority** unless you applied `-s` / `-sr` / shuffle.
- **`-aa` approx aggregate** can include contiguous IPs not in the input — annotate when used.
- **ASN expansion** is cloud-backed; local runs without API key fail fatally.
- **Relations** — use ontology `contains` (not invented `CONTAINS_IP`).
- **IP nugget ids** — create addresses only via `classify_ip` (never hardcode ambiguous `IP_ADDRESS` for colon-form IPv6).

## Strategies and Tactics

**Normalize → slice → scan**

```
authorized CIDRs → mapcidr -silent (-sbc/-sbh as needed) → naabu/nmap/httpx
```

**Aggregate noisy IP lists**

```
IP list → mapcidr -a -silent → fewer CIDR targets for reporting / scanners
```

**Differential updates**

1. Re-expand latest authorized blocks.
2. Diff against prior host snapshot.
3. Scan net-new hosts first.

See `references/tactics.md` for full playbooks.

## Comprehensive Examples

### Version and help

```bash
mapcidr -version
mapcidr -h
```

### Expand CIDR (stdin or `-cidr`)

```bash
echo "10.0.0.0/30" | mapcidr -silent
mapcidr -cidr 173.0.84.0/24 -silent
```

### File / multi input

```bash
mapcidr -cl cidrs.txt -silent -o expanded.txt
```

### IP range

```bash
echo "192.168.0.0-192.168.0.5" | mapcidr -silent
```

### Slice by CIDR count / host count

```bash
mapcidr -cidr 10.0.0.0/24 -sbc 4 -silent
mapcidr -cidr 10.0.0.0/24 -sbh 64 -silent
```

### Aggregate / approx aggregate

```bash
mapcidr -cl cidrs.txt -a -silent
printf "1.1.1.1\n1.1.1.16\n1.1.1.31\n" | mapcidr -aa -silent
```

### Count

```bash
echo "173.0.84.0/16" | mapcidr -c -silent
```

### Skip base / broadcast; match / filter

```bash
mapcidr -cidr 10.0.0.0/29 -skip-base -skip-broadcast -silent
mapcidr -cidr 192.168.1.0/24 -mi 192.168.1.1,192.168.1.2 -silent
mapcidr -cidr 192.168.1.224/28 -fi 192.168.1.233,192.168.1.234 -silent
```

### IPv4/IPv6 convert and family filter

```bash
mapcidr -cl ips.txt -t6 -silent
echo "00:00:00:00:00:ffff:0101:0101" | mapcidr -t4 -silent
printf "1.1.1.1\n2001:db8::1\n" | mapcidr -f4 -silent
printf "1.1.1.1\n2001:db8::1\n" | mapcidr -f6 -silent
```

### IP formats / shuffle port

```bash
echo "127.0.1.0" | mapcidr -if 0 -silent
echo "1.1.1.1" | mapcidr -sp 80,443 -silent
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Captured help, all flags |
| `output-and-parsing.md` | Line shapes → JSON bundle parsing |
| `nugget-mapping.md` | Lines → SpiderFeet graph |
| `tactics.md` | Sequencing and pivots |
| `sources.md` | Official URLs |

**Operator docs:** `.docs/docs-for-cli-tools/mapcidr-Zero-to-Hero.md`, `.docs/docs-for-cli-tools/mapcidr-CLI-Options.md`.
