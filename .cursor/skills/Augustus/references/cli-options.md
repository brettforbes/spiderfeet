# Augustus CLI Options

## Core commands

- `augustus scan <generator>`
- `augustus list`
- `augustus version`
- `augustus completion <shell>`

## Probe selection

- `--probe`, `-p` (repeatable)
- `--probes-glob`
- `--all`

## Detector selection

- `--detector` (repeatable)
- `--detectors-glob`

## Buff selection

- `--buff`, `-b` (repeatable)
- `--buffs-glob`

## Execution tuning

- `--harness`
- `--timeout`
- `--probe-timeout`
- `--concurrency`

## Configuration

- `--config-file` (YAML)
- `--config`, `-c` (JSON)

## Output

- `--format table|json|jsonl`
- `--output`, `-o` (JSONL file)
- `--html` (report file)
- `--verbose`, `-v`
- `--debug`, `-d`

## Examples

```bash
augustus list
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN --format jsonl -o out.jsonl
augustus scan openai.OpenAI --probes-glob "dan.*,grandma.*" --detectors-glob "*" --config-file config.yaml --output batch.jsonl
augustus scan openai.OpenAI --all --buffs-glob "encoding.*,paraphrase.*" --timeout 60m --html report.html
augustus completion zsh
```
