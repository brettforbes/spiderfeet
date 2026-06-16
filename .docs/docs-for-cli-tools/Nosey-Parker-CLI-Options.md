# Nosey-Parker CLI Options

## Core commands

- `noseyparker scan`
- `noseyparker report`
- `noseyparker summarize` (if supported)

## Common option classes

- `--datastore <path>`
- Scope include/exclude controls
- Output format flags
- Verbose/logging flags

## Examples

```bash
noseyparker scan --datastore ./np-ds ./repo
noseyparker report --datastore ./np-ds --format json > findings.json
```
