# tldfinder CLI Options

Quick option reference for `tldfinder`. Validate exact switches with `tldfinder -h`.

## Standard option classes

| Class | Typical options | Purpose |
|---|---|---|
| Seed input | `-d`, `-l` | Provide initial domains/targets |
| Output mode | `-json` | Structured parser-friendly output |
| Basic run controls | verbosity/silent flags | Human vs automated operation |

## Advanced option classes

| Class | Typical options | Purpose |
|---|---|---|
| Confidence filters | threshold/min-score flags | Keep high-signal candidates |
| Resolver selection | `-r` | Validate from specific resolver sets |
| Runtime tuning | concurrency/rate flags | Scale large runs safely |

## Examples by major option class

```bash
# Single seed
tldfinder -d example.com -json

# Seed list
tldfinder -l seeds.txt -json

# Confidence-filtered run
tldfinder -l seeds.txt -json -min-confidence 0.7

# Resolver-controlled pass
tldfinder -l seeds.txt -json -r resolvers.txt
```

## Conversion reminder

Map parsed findings to SpiderFeet graph payloads:
- `nodes[]`: seed and candidate namespace/host nodes
- `edges[]`: `suggests_private_tld`, `expands_to_candidate_host`

Reference: `.cursor/skills/tldfinder/references/nugget-mapping.md`.
