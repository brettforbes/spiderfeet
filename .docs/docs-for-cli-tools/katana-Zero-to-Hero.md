# katana Zero-to-Hero

## Start

```bash
katana -u https://example.org -silent -jsonl
```

## Progression

1. Crawl baseline targets.
2. Add depth/scope control.
3. Enable JS crawl (`-jc`) for SPAs.
4. Enable `-kf`/`-fx` for deeper discovery.
5. Parse JSONL and convert to graph nodes/edges.

## Practical Examples

```bash
katana -u https://example.org -silent -jsonl -depth 3
katana -u https://app.example.org -silent -jsonl -jc -depth 4
katana -list targets.txt -silent -jsonl -kf all -fx
```

## Conversion Guidance

- URL -> `URL` node.
- Host -> `INTERNET_NAME` node.
- Host to URL -> `DISCOVERED_URL` edge.
