# Vespasian Tactics and Workflows

## Workflow A: Fast recon

1. `scan` with default `auto` API detection.
2. Review generated spec and endpoint count.
3. Re-run with auth headers and deeper crawl if surface looks thin.

## Workflow B: Repeatable pipeline

1. `crawl` (or `import`) to produce stable `capture.json`.
2. Run `generate` per API type as needed.
3. Version-control capture/spec artifacts for team review and diffing.

## Workflow C: Proxy-assisted testing

1. Route scan via intercepting proxy.
2. Drive auth flows manually if needed.
3. Import traffic artifacts and regenerate specs.

## Tactics

- Use same-origin first; expand to same-domain only when justified.
- Keep probing on for richer endpoint metadata.
- Use confidence threshold tuning to reduce false positives.
- For GraphQL, leverage captured operations when introspection is blocked.
