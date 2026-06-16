# mapcidr CLI Options

## Primary

- `-l` input file
- `-o` output file
- stdin pipeline support

## Operational Usage

- CIDR/range expansion
- normalization and dedup in shell pipeline
- chunking strategy externalized as needed

## Examples

```bash
echo "10.0.0.0/24" | mapcidr
mapcidr -l ranges.txt -o expanded.txt
cat ranges.txt | mapcidr | sort -u > expanded.txt
```
