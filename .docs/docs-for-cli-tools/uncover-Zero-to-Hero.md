# uncover Zero-to-Hero

## First Query

```bash
uncover -q 'ssl:"example.org"' -e shodan
```

## Progression

1. Configure provider API access.
2. Run focused single-provider queries.
3. Expand to multi-provider correlation.
4. Normalize outputs and deduplicate.
5. Validate high-value findings with direct scanners.

## Examples

```bash
uncover -q 'title:"admin"' -e shodan -silent
uncover -q 'product:"nginx" port:443' -e shodan,censys,fofa -silent
uncover -q 'domain:"example.org"' -e netlas
```

## Nugget Conversion

- host -> `IP_ADDRESS` or `INTERNET_NAME`
- service -> `TCP_PORT_OPEN`
- evidence metadata retains provider provenance
