# Augustus CLI Options

## Main commands

- `augustus scan <generator>`
- `augustus list`
- `augustus version`
- `augustus completion <shell>`

## Scan option groups

### Probe selection
- `--probe`, `-p`
- `--probes-glob`
- `--all`

### Detector selection
- `--detector`
- `--detectors-glob`

### Buff selection
- `--buff`, `-b`
- `--buffs-glob`

### Configuration
- `--config-file`
- `--config`, `-c`

### Runtime
- `--harness`
- `--timeout`
- `--probe-timeout`
- `--concurrency`

### Output and logs
- `--format table|json|jsonl`
- `--output`, `-o`
- `--html`
- `--verbose`, `-v`
- `--debug`, `-d`

## Example commands

```bash
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN --format json
augustus scan openai.OpenAI --all --concurrency 20 --timeout 60m --output all.jsonl
augustus scan rest.Rest --probe dan.Dan_11_0 --config-file rest.yaml --html report.html
augustus list
augustus completion bash
```

## Exit behavior

Use command return code and output files together for CI gating. Parse JSON/JSONL instead of table output in automation paths.
