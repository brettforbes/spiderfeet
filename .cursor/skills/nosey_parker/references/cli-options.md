# nosey_parker CLI Options

Verify exact options with `noseyparker --help` for your installed version.

## Core commands

- `noseyparker scan`
- `noseyparker report`
- `noseyparker summarize` (if supported)

## Common option classes

- `--datastore <path>`
- Scope include/exclude filters
- Output format flags (`json`/`jsonl` where supported)
- Verbosity/logging controls

## Examples

```bash
noseyparker scan --datastore ./np-ds ./repo
noseyparker report --datastore ./np-ds
noseyparker report --datastore ./np-ds --format json > findings.json
```
