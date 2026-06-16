# Titus CLI Options

## Core commands

- `titus scan <path...>`
- `titus version` (if supported)

## Common option classes

- Scope include/exclude controls
- Output format options
- Confidence/filter options
- Verbose/debug and performance controls

## Examples

```bash
titus scan ./repo
titus scan ./repo --format json > findings.json
titus scan ./repo --verbose
```
