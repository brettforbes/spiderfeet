# NTLMRecon CLI Options

## Command pattern

```bash
ntlmrecon [target/options]
```

## Common option classes

- Target selection (`-t`, list mode)
- Protocol and port controls
- Timeout/retry tuning
- Verbose/debug output options

## Examples

```bash
ntlmrecon -t 10.10.10.20
ntlmrecon -i targets.txt
ntlmrecon -t dc01.corp.local -v
```
