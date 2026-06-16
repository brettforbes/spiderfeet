# uncover CLI Options

## Core

- `-q` query/dork text
- `-e` engine/provider selection
- `-silent` compact output

## Provider/Config

- provider credentials from env/config
- single or multi-provider runs
- rate/concurrency behavior by provider/build

## Examples

```bash
uncover -q 'ssl:"example.org"' -e shodan
uncover -q 'product:"nginx" port:443' -e shodan,censys,fofa -silent
uncover -q 'domain:"example.org"' -e netlas
```
