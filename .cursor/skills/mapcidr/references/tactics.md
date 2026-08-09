# mapcidr Strategies, Tactics, and Workflows

## Strategy: normalize once, scan many

Use mapcidr early to turn messy netblock/IP inputs into **deduped, sized, and sliced** target sets. Prefer `-silent` line capture, then parse to a JSON `records[]` bundle for SpiderFeet.

Always start with sizing before blasting huge spaces:

```bash
echo "203.0.113.0/16" | mapcidr -c -silent
```

## Workflow 1 — Expand authorized CIDRs to host queue

1. Collect authorized CIDRs/ranges (RIR, Pius, inventory).
2. Expand: `mapcidr -cl cidrs.txt -silent -o hosts.txt`.
3. Optional: `-skip-base -skip-broadcast` for coarse IPv4 noise reduction.
4. Deduplicate: `sort -u`.
5. Parse → nuggets (`NETBLOCK_*` `contains` addresses).
6. Feed hosts to naabu/nmap/httpx in chunks.

## Workflow 2 — Slice for load distribution

1. Count hosts (`-c`).
2. If too large, slice:
   - equal-ish CIDR pieces: `-sbc N`
   - host-budget pieces: `-sbh N`
3. Assign each output CIDR to a scanner worker/batch.
4. Keep sliced CIDRs (do not always expand to every IP) when the next tool accepts CIDR input.

```bash
mapcidr -cidr 10.0.0.0/16 -sbh 4096 -silent -o slices.txt
```

## Workflow 3 — Aggregate sparse IP hits

1. Take unique IPs from uncover/naabu/passive sources.
2. `mapcidr -cl ips.txt -a -silent` for exact minimum subnets.
3. Use `-aa` only when sparse IPv4 grouping is acceptable (may cover non-input IPs).
4. Map output CIDRs as `NETBLOCK_OWNER` for reporting and follow-on scans.

## Workflow 4 — Family and format controls

| Goal | Flags |
|------|--------|
| IPv4-only queue | `-f4` (spot-check keep behavior) |
| IPv6-only queue | `-f6` |
| IPv4-mapped → IPv4 | `-t4` |
| IPv4 → IPv4-mapped IPv6 | `-t6` |
| Obfuscation/format research | `-if 0` or specific index |
| IP:port target list | `-sp 80,443` |

## Workflow 5 — Match / filter intersections

```bash
mapcidr -cidr 192.168.1.0/24 -mi allow.txt -silent
mapcidr -cidr 192.168.1.0/24 -fi deny.txt -silent
```

Use for allow-list intersection and deny-list subtraction before active scanning.

## Workflow 6 — Differential updates

1. Snapshot expanded hosts for the engagement.
2. Re-run mapcidr when netblocks change.
3. Diff sets; scan net-new hosts first.
4. Re-aggregate when IP lists grow sparse/noisy.

## Tactical adaptations

| Observation | Adaptation |
|-------------|------------|
| Output millions of hosts | Stop; `-c` then `-sbc`/`-sbh`; do not pipe raw expand into scanners |
| Overlapping CIDRs | Expand + dedupe; multi-parent `contains` edges OK |
| ASN input fails with 401 | Configure pdcp via `-auth` or skip ASN scenario as blocked |
| Downstream tool wants CIDRs | Prefer slice/aggregate output over full expand |
| Need random scan order | `-si` or `-sp` (ports) — document non-reproducibility |
| Formal examination | `-silent` + full capture + JSON bundle + graph + narrative |

## Sequencing with other SpiderFeet skills

```
pius/uncover/RIR CIDRs
        → mapcidr (-c / -sbc / -sbh / -a as needed) -silent
        → naabu | nmap | httpx | dnsx (PTR)
        → nerva / nuclei (on live services)
```

## Exploration vs examination

| Phase | Output |
|-------|--------|
| Exploration | Try expand, slice, aggregate, filter, count; note shapes |
| Formal examination | `-silent` line capture → parse to JSON bundle → graph + narrative mandatory |

**JSON preference:** if a future mapcidr release adds a JSON flag, switch formal runs to that flag immediately. Until then, structured = harvested bundle from lines.
