# Metasploit CLI Options (Package Summary)

**Version:** metasploit-framework **6.5.2-20260809060523-1rapid7**  
**Tree:** `.tools/metasploit/framework/`  
**Flag source of truth:** Reconstructed OptionParser help emitted **2026-08-10** (embedded `ruby.exe` + package `parsed_options` / msfvenom / msfdb sources). Live `msf*.bat -h` failed with `Bundler::GemNotFound` after MSI admin extract; full MSI install also failed (**1603**).

Full combined capture (failure snippets + verbatim reconstructed help + companion bins):  
`.docs/docs-for-cli-tools/Metasploit-Framework-CLI-Options.md`

Do **not** invent flags beyond that document.

## Quick reference — msfconsole

| Flag | Purpose |
|------|---------|
| `-a`, `--ask` | Ask before exit / accept `exit -y` |
| `-H`, `--history-file FILE` | Command history file |
| `-l`, `--logger STRING` | Logger |
| `--[no-]readline` | Readline toggle |
| `-L`, `--real-readline` | System Readline vs RbReadline |
| `-o`, `--output FILE` | Output file |
| `-p`, `--plugin PLUGIN` | Load plugin on startup |
| `-q`, `--quiet` | No banner |
| `-r`, `--resource FILE` | Resource script (`-` = stdin) |
| `-x`, `--execute-command COMMAND` | Console commands (`;` separates) |
| `-E`, `--environment ENVIRONMENT` | Rails env (default production / `RAILS_ENV`) |
| `-M`, `--migration-path DIRECTORY` | Extra DB migrations |
| `-n`, `--no-database` | Disable database |
| `-y`, `--yaml PATH` | DB YAML settings |
| `-c FILE` | Config file |
| `-v`, `-V`, `--version` | Version |
| `--[no-]defer-module-loads` | Defer module loading |
| `-m`, `--module-path DIRECTORY` | Extra module path |
| `-h`, `--help` | Help |

## Quick reference — msfvenom

| Flag | Purpose |
|------|---------|
| `-l`, `--list <type>` | List payloads, encoders, nops, platforms, archs, encrypt, formats, all |
| `-p`, `--payload <payload>` | Payload (`-` / STDIN for custom) |
| `--list-options` | Payload standard/advanced/evasion options |
| `-f`, `--format <format>` | Output format |
| `-e`, `--encoder <encoder>` | Encoder |
| `--service-name`, `--sec-name`, `--smallest` | Binary / size helpers |
| `--encrypt`, `--encrypt-key`, `--encrypt-iv` | Shellcode encryption |
| `-a`, `--arch`, `--platform` | Arch / platform |
| `-o`, `--out <path>` | Output file |
| `-b`, `--bad-chars`, `-n`, `--nopsled`, `--pad-nops` | Encoding constraints |
| `-s`, `--space`, `--encoder-space`, `-i`, `--iterations` | Size / encode loops |
| `-c`, `--add-code`, `-x`, `--template`, `-k`, `--keep` | Code / template inject |
| `-v`, `--var-name`, `-t`, `--timeout` | Format / STDIN timeout |
| `--refresh-cache` | Rebuild module metadata cache |
| `-h`, `--help` | Help |

Payload datastore as trailing `var=val` (e.g. `LHOST=… LPORT=…`).

## Quick reference — msfdb

**Commands:** `init`, `reinit`, `delete`, `status`, `start`, `stop`, `restart`

| Flag area | Examples |
|-----------|----------|
| General | `--component database\|webservice`, `-d`, `--use-defaults`, `-h` |
| Database | `--msf-db-name`, `--msf-db-user-name`, `--db-port`, `--db-pool`, `--connection-string` |
| Webservice | `-a`, `-p`, `--[no-]daemon`, `--[no-]ssl`, `--user`, `--pass`, … |

## Companion `bin/*.bat` (this package)

Present under `.tools/metasploit/framework/bin/`: `msfconsole`, `msfvenom`, `msfdb`, `msfrpcd`, `msfrpc`, `msfupdate`, `msfd`, scanners (`msfbinscan`, `msfelfscan`, `msfmachscan`, `msfpescan`), `msfrop`, `msfremove`. Only msfconsole / msfvenom / msfdb OptionParser help was reconstructed for this skill pass.
