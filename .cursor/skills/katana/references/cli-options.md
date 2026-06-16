# Katana CLI Options

## Core

- `-u` single target URL
- `-list` input file/list
- `-silent` quiet mode
- `-jsonl` machine-readable output
- `-depth` crawl depth
- `-concurrency` parallel workers
- `-timeout` request timeout
- `-retry` retries

## Discovery/Extraction

- `-jc` JavaScript crawl
- `-hl` headless crawl mode
- `-fx` form extraction
- `-kf` known files probing

## Filtering and Scope

- include/exclude regex controls
- host/domain scope boundaries
- extension/content filtering

## Example Classes

```bash
katana -u https://example.org -silent -jsonl
katana -u https://example.org -silent -jsonl -depth 2 -concurrency 5
katana -u https://spa.example.org -silent -jsonl -jc -depth 4
```
