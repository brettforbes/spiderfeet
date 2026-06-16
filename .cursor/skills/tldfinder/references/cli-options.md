# tldfinder CLI Options

`tldfinder` evolves quickly; check `tldfinder -h` for your installed binary.

## Major option classes

| Class | Typical usage shape | Purpose |
|---|---|---|
| Seed input | domain/org/list flags | Provide starting namespace indicators |
| Output format | JSON/text flags | Prefer parser-safe structured output |
| Confidence/filtering | threshold/filter flags | Remove weak candidates |
| Resolver/network | resolver/proxy/runtime flags | Stabilize results by vantage |
| Performance | concurrency/rate controls | Scale safely for large seed sets |

## Examples by option class

```bash
# Basic run from seed domain
tldfinder -d example.com -json

# Batch seeds from file
tldfinder -l seeds.txt -json

# Filtered/high-confidence run (if supported)
tldfinder -l seeds.txt -json -min-confidence 0.7

# Resolver-specific validation
tldfinder -l seeds.txt -json -r resolvers.txt
```

## Practical usage notes

- Use structured output whenever possible for repeatable automation.
- Retain candidate confidence/score fields during transformation.
- Re-run high-value findings through `dnsx` for active validation.
