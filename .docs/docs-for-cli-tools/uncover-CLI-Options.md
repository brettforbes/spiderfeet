# uncover CLI Options

## Core

- `-q` query/dork
- `-e` provider engines
- `-silent` concise mode

## Usage Patterns

- single-provider focused reconnaissance
- multi-provider corroboration
- query narrowing by domain, org, product, port

## Examples

```bash
uncover -q 'ssl:"example.org"' -e shodan
uncover -q 'title:"login" port:443' -e shodan,censys -silent
uncover -q 'domain:"example.org"' -e netlas
```
