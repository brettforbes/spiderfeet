# mapcidr CLI Options

## Core

- `-l` input file
- `-o` output file
- stdin support for pipelines

## Processing

- CIDR/range expansion
- normalization helpers
- split/chunk strategies (workflow dependent)
- IPv4/IPv6 controls (build dependent)

## Examples

```bash
echo "192.0.2.0/30" | mapcidr
mapcidr -l netblocks.txt -o hosts.txt
cat ranges.txt | mapcidr | sort -u > hosts.txt
```
