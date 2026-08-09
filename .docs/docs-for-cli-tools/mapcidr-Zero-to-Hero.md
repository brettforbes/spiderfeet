# mapcidr Zero to Hero

Practical guide for using **mapcidr** to expand, slice, and aggregate CIDRs/IP ranges, then feed SpiderFeet recon workflows. Flags validated against the local binary on **2026-08-10**.

Skill reference: `.cursor/skills/mapcidr/SKILL.md`

**Binary (this repo):** `C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe` — **v1.1.97** (help captured **2026-08-10**).

## What mapcidr does

mapcidr (ProjectDiscovery) is a **netblock utility** for mass-scan load distribution. It expands CIDRs and IP ranges to hosts, slices large blocks into smaller CIDRs, aggregates IP/CIDR lists into minimum subnets, counts hosts, filters/matches, converts IPv4↔IPv6 forms, and can emit IP:port shuffles.

mapcidr does **not**:

- Port-scan or service-fingerprint (use **naabu** / **nmap** / **nerva**)
- Resolve DNS (use **dnsx**)
- Probe HTTP (use **httpx**)
- Emit native JSON on this binary (parse `-silent` lines into a harvest bundle)

---

## Level 0 — Install and verify

```bash
go install -v github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest
mapcidr -version
mapcidr -h
```

Or: https://github.com/projectdiscovery/mapcidr/releases

This workspace:

```powershell
& "C:\projects\spiderfeet\.tools\mapcidr\mapcidr.exe" -version
```

---

## Level 1 — First expansion

```bash
echo "203.0.113.0/30" | mapcidr -silent
```

Or:

```bash
mapcidr -cidr 203.0.113.0/30 -silent
```

Output: one IP per line (`203.0.113.0` … `203.0.113.3`).

---

## Level 2 — Files, ranges, and output files

```bash
mapcidr -cl cidrs.txt -silent -o expanded.txt
echo "192.168.0.0-192.168.0.5" | mapcidr -silent
```

Input flag is **`-cl` / `-cidr`** (file path, CIDR, or IP). There is no `-l` in help.

---

## Level 3 — Count before you explode

```bash
echo "203.0.113.0/16" | mapcidr -c -silent
```

Prints a single integer (e.g. `65536`). Always count large blocks before expanding into scanners.

---

## Level 4 — Slice for load distribution

By number of CIDR pieces:

```bash
mapcidr -cidr 10.0.0.0/24 -sbc 4 -silent
```

By host budget per piece:

```bash
mapcidr -cidr 10.0.0.0/24 -sbh 64 -silent
```

Feed each resulting CIDR to a separate scanner batch. Perfect splits are easiest when counts are powers of two (upstream README).

---

## Level 5 — Aggregate and approx-aggregate

Exact minimum subnets:

```bash
mapcidr -cl cidrs.txt -a -silent
```

Sparse IPv4 approx (may cover contiguous IPs not in the input):

```bash
printf "1.1.1.1\n1.1.1.16\n1.1.1.31\n" | mapcidr -aa -silent
```

Example result: `1.1.1.0/27`.

---

## Level 6 — Filters, match, family controls

```bash
mapcidr -cidr 10.0.0.0/29 -skip-base -skip-broadcast -silent
mapcidr -cidr 192.168.1.0/24 -mi 192.168.1.1,192.168.1.2 -silent
mapcidr -cidr 192.168.1.224/28 -fi 192.168.1.233,192.168.1.234 -silent
printf "1.1.1.1\n2001:db8::1\n" | mapcidr -f4 -silent
printf "1.1.1.1\n2001:db8::1\n" | mapcidr -f6 -silent
```

Spot-check `-f4`/`-f6` on a tiny mixed sample before production use.

---

## Level 7 — Convert, formats, ports, sort

```bash
echo "1.1.1.1" | mapcidr -t6 -silent
echo "00:00:00:00:00:ffff:0101:0101" | mapcidr -t4 -silent
echo "127.0.1.0" | mapcidr -if 0 -silent
echo "1.1.1.1" | mapcidr -sp 80,443 -silent
printf "10.0.0.3\n10.0.0.1\n" | mapcidr -s -silent
```

IP format index details: [IP-Format-Index wiki](https://github.com/projectdiscovery/mapcidr/wiki/IP-Format-Index).

---

## Level 8 — Structured capture for SpiderFeet

This binary has **no `-json` flag**. Formal workflow:

1. Run with `-silent` (and `-o` if useful).
2. Parse each line into `records[]` (`schema: mapcidr_lines_v1`).
3. Derive human Text from those records.
4. Build nugget graph + narrative from the structured bundle.

See `.cursor/skills/mapcidr/references/output-and-parsing.md`.

---

## Level 9 — Nugget mapping (hero)

| Artifact | Nugget |
|----------|--------|
| Source / output CIDR (v4) | `NETBLOCK_OWNER` |
| Source / output CIDR (v6) | `NETBLOCKV6_OWNER` |
| Host IP | `classify_ip` → `IPV4_ADDRESS` / `IPV6_ADDRESS` / `INTERNAL_IP_ADDRESS` |
| `ip:port` | address + `TCP_PORT_OPEN` when port present |

Relation: netblock **`contains`** address. Full rules: `.cursor/skills/mapcidr/references/nugget-mapping.md`.

---

## Level 10 — Pipelines

```bash
# Expand → unique hosts → naabu
mapcidr -cl cidrs.txt -silent | sort -u | naabu -silent -json

# Slice first for large space
mapcidr -cidr 10.0.0.0/16 -sbh 4096 -silent -o slices.txt
# then scan each line in slices.txt

# Aggregate passive IPs → CIDR report
sort -u ips.txt | mapcidr -a -silent
```

Typical chain:

```
pius/uncover CIDRs → mapcidr → naabu/nmap → httpx/nerva/nuclei
```

---

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Invented `-l` / `-json` | Use `-cl`/`-cidr`; parse lines |
| Expanding /8 without planning | `-c` then `-sbc`/`-sbh` |
| ASN `401 unauthorized` | Configure pdcp (`-auth`) or skip |
| Treating `-aa` as exact membership | Annotate approx coverage |
| Graph without structured parse | Bundle `records[]` first; graph mandatory |

---

## Next docs

- Full flag tables: `mapcidr-CLI-Options.md`
- Skill + references: `.cursor/skills/mapcidr/`
