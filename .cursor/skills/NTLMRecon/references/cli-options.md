# NTLMRecon CLI Options

Verify available flags with `ntlmrecon -h`.

## Command shape

```bash
ntlmrecon [target/options]
```

## Common option classes

- Target selection options (`-t`, list mode variants)
- Protocol/port controls
- Timeout/retry tuning
- Verbose/debug output controls

## Examples

```bash
ntlmrecon -t 10.10.10.20
ntlmrecon -i targets.txt
ntlmrecon -t dc01.corp.local -v
```
