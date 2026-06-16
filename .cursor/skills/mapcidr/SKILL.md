---
name: mapcidr
description: Expand and normalize CIDRs/ranges with mapcidr, then convert results into SpiderFeet netblock and host graph artifacts. Trigger on mapcidr, CIDR expansion, IP-range splitting, netblock preprocessing, or host-target generation for recon pipelines.
---

# mapcidr

## Purpose

Use mapcidr to transform netblocks into clean host target sets and map outputs to SpiderFeet nuggets and edges.

## Step-by-Step Instructions

1. Confirm authorized netblock scope.
2. Ingest CIDR/range input from stdin or file.
3. Run mapcidr expansion/normalization.
4. De-duplicate overlapping outputs.
5. Chunk large output for downstream tools.
6. Convert into `NETBLOCK_OWNER` and `IP_ADDRESS` graph artifacts.

### Examples

```bash
echo "10.10.0.0/24" | mapcidr
mapcidr -l cidrs.txt -o expanded.txt
cat cidrs.txt | mapcidr | sort -u > unique_hosts.txt
```

## If/Then Decision Rules

- If netblock is too large, then split/chunk before downstream scans.
- If ranges overlap, then deduplicate hosts before graph emission.
- If downstream is IPv4-only, then filter IPv6 outputs.
- If parsing line fails, then skip line and continue.

## Guardrails & Pitfalls

- Authorized scope only.
- Avoid exploding large ranges without execution controls.
- Preserve provenance (source CIDR/range) for each host.
- Do not assume output order equals priority.

## references

- `references/SKILLS.md`
- `references/cli-options.md`
- `references/output-and-parsing.md`
- `references/nugget-mapping.md`
- `references/tactics.md`
- `references/sources.md`
