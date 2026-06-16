# mapcidr Zero-to-Hero

## First Command

```bash
echo "203.0.113.0/30" | mapcidr
```

## Progression

1. Expand single CIDRs.
2. Process bulk files.
3. Deduplicate and chunk outputs.
4. Convert to nugget graph artifacts.
5. Feed live hosts to discovery/fingerprint tools.

## Examples

```bash
mapcidr -l netblocks.txt -o hosts.txt
cat netblocks.txt | mapcidr | sort -u > unique_hosts.txt
```

## Nugget Conversion

- netblock input -> `NETBLOCK_OWNER`
- host output -> `IP_ADDRESS`
- relationship -> `CONTAINS_IP`
