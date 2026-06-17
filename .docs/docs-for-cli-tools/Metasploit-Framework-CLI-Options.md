# Metasploit Framework CLI and Console Options

## `msfconsole`
- `-r <file>` run resource script
- `-x <cmds>` execute command string
- `-q` quiet mode

## `msfvenom`
- List payloads/platforms/formats/encoders
- Common generation flags: payload, platform, arch, format, output, badchars, encoder, iterations, LHOST/LPORT

## `msfdb`
- `init`, `start`, `stop`, `status`, `reinit`

## Console command families
- `search`, `use`, `info`, `show`, `set`, `unset`
- `run`, `check`, `exploit`
- `sessions`
- `workspace`
- `db_*`, `hosts`, `services`, `vulns`, `loot`, `creds`

## Recommended operation
Always inspect `info` + `show options/advanced/evasion` before execution, and keep workspace segmentation strict for each engagement.
