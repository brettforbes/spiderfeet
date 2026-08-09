# Metasploit Framework CLI Options

Operator reference for **msfconsole**, **msfvenom**, and **msfdb** on the SpiderFeet nightly Windows package, plus notes on companion `bin/*.bat` tools.

SpiderFeet preferred discovery automation (when runtime works):

```bash
msfdb init --use-defaults
msfconsole -q -r discover.rc
msfconsole -q -x "workspace lab1; use auxiliary/scanner/smb/smb_version; set RHOSTS 192.168.56.0/24; run; hosts"
```

| Field | Value |
|-------|-------|
| Version | **metasploit-framework 6.5.2-20260809060523-1rapid7** |
| Package tree | `C:\projects\spiderfeet\.tools\metasploit\framework\` |
| Capture date | **2026-08-10** |
| Live help attempts | `.tmp_msf_help/msfconsole_h.txt`, `msfvenom_h.txt`, `msfdb_h.txt` |
| Authoritative flags | `.tmp_msf_help/msf*_help_reconstructed.txt` (OptionParser) |
| Optional shipped doc | `.tmp_msf_help/msfconsole.md` |
| Reconstruction script | `.tmp_msf_help/emit_help.rb` |

> **Do not invent flags.** Process argv below is exactly the reconstructed OptionParser output from this package on **2026-08-10**. Interactive console commands (`search`, `hosts`, …) are documented in a separate section — they are not `msfconsole` CLI switches.

Skill: `.cursor/skills/metasploit_framework/SKILL.md`

---

## Package / version

```text
metasploit-framework 6.5.2-20260809060523-1rapid7

Component                               Installed Version              Version GUID                                                              
-------------------------------------------------------------------------------------------------------------------------------------------------
bundler                                 2.6.7                          
```

Source: `.tmp_msf_help/version.txt`.

---

## Captured failure (live runtime)

After **MSI admin extract** into `.tools/metasploit/framework/`, invoking the wrapper bats fails during Bundler setup. A **full MSI install** on this host also failed with **Windows Installer error 1603** (see `.tools/metasploit/msiexec-full.log`). Live `-h` is therefore **not** available from this tree; flags were reconstructed from package OptionParser definitions via embedded `ruby.exe`.

### Snippet — `msfconsole -h` (`.tmp_msf_help/msfconsole_h.txt`)

```text
Bundler::Definition#materialize': Could not find simplecov-0.18.2, redcarpet-3.6.1, yard-0.9.37, ... in locally installed gems (Bundler::GemNotFound)
	from .../bundler/definition.rb:193:in 'Bundler::Definition#specs'
	...
	from .../embedded/framework/msfconsole:17:in '<main>'
```

### Snippet — `msfvenom -h` (`.tmp_msf_help/msfvenom_h.txt`)

```text
Bundler::Definition#materialize': Could not find simplecov-0.18.2, redcarpet-3.6.1, yard-0.9.37, ... in locally installed gems (Bundler::GemNotFound)
	...
	from .../embedded/framework/msfvenom:5:in '<main>'
```

### Snippet — `msfdb -h` (`.tmp_msf_help/msfdb_h.txt`)

```text
WARN: Unresolved or ambiguous specs during Gem::Specification.reset:
      base64 (>= 0.2)
      logger (~> 1.6)
...
Bundler::Definition#materialize': Could not find simplecov-0.18.2, redcarpet-3.6.1, yard-0.9.37, ... in locally installed gems (Bundler::GemNotFound)
	...
	from .../embedded/framework/msfdb:32:in '<main>'
```

### Related — `msfupdate` (`.tmp_msf_help/msfupdate_h.txt`)

```text
Downloading latest Metasploit Framework
Updating Metasploit Framework
Metasploit update failed, error code: 1602
```

---

## Reconstructed OptionParser help (authoritative flags)

Emitted **2026-08-10** from this package’s OptionParser definitions (`parsed_options` + msfvenom/msfdb sources) using embedded `ruby.exe` — see `.tmp_msf_help/emit_help.rb`. These blocks are the **authoritative CLI flag lists** for this package while live bats cannot boot.

### `msfconsole` (`.tmp_msf_help/msfconsole_help_reconstructed.txt`)

```text
Usage: msfconsole [options]

Console options:
    -a, --ask                        Ask before exiting Metasploit or accept 'exit -y'
    -H, --history-file FILE          Save command history to the specified file
    -l, --logger STRING              Specify a logger to use
        --[no-]readline
    -L, --real-readline              Use the system Readline library instead of RbReadline
    -o, --output FILE                Output to the specified file
    -p, --plugin PLUGIN              Load a plugin on startup
    -q, --quiet                      Do not print the banner on startup
    -r, --resource FILE              Execute the specified resource file (- for stdin)
    -x, --execute-command COMMAND    Execute the specified console commands (use ; for multiples)

Common options:
    -E, --environment ENVIRONMENT    Set Rails environment, defaults to RAIL_ENV environment variable or 'production'

Database options:
    -M, --migration-path DIRECTORY   Specify a directory containing additional DB migrations
    -n, --no-database                Disable database support
    -y, --yaml PATH                  Specify a YAML file containing database settings

Framework options:
    -c FILE                          Load the specified configuration file
    -v, -V, --version                Show version

Module options:
        --[no-]defer-module-loads    Defer module loading unless explicitly asked
    -m, --module-path DIRECTORY      Load an additional module path

    -h, --help                       Show this message
```

### `msfvenom` (`.tmp_msf_help/msfvenom_help_reconstructed.txt`)

```text
MsfVenom - a Metasploit standalone payload generator.
Also a replacement for msfpayload and msfencode.
Usage: msfvenom [options] <var=val>
Example: msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> -f exe -o payload.exe

Options:
    -l, --list            <type>     List all modules for [type]. Types are: payloads, encoders, nops, platforms, archs, encrypt, formats, all
    -p, --payload         <payload>  Payload to use (--list payloads to list, --list-options for arguments). Specify '-' or STDIN for custom
        --list-options               List --payload <value>'s standard, advanced and evasion options
    -f, --format          <format>   Output format (use --list formats to list)
    -e, --encoder         <encoder>  The encoder to use (use --list encoders to list)
        --service-name    <value>    The service name to use when generating a service binary
        --sec-name        <value>    The new section name to use when generating large Windows binaries. Default: random 4-character alpha string
        --smallest                   Generate the smallest possible payload using all available encoders
        --encrypt         <value>    The type of encryption or encoding to apply to the shellcode (use --list encrypt to list)
        --encrypt-key     <value>    A key to be used for --encrypt
        --encrypt-iv      <value>    An initialization vector for --encrypt
    -a, --arch            <arch>     The architecture to use for --payload and --encoders (use --list archs to list)
        --platform        <platform> The platform for --payload (use --list platforms to list)
    -o, --out             <path>     Save the payload to a file
    -b, --bad-chars       <list>     Characters to avoid example: '\x00\xff'
    -n, --nopsled         <length>   Prepend a nopsled of [length] size on to the payload
        --pad-nops                   Use nopsled size specified by -n <length> as the total payload size, auto-prepending a nopsled of quantity (nops minus payload length)
    -s, --space           <length>   The maximum size of the resulting payload
        --encoder-space   <length>   The maximum size of the encoded payload (defaults to the -s value)
    -i, --iterations      <count>    The number of times to encode the payload
    -c, --add-code        <path>     Specify an additional win32 shellcode file to include
    -x, --template        <path>     Specify a custom executable file to use as a template
    -k, --keep                       Preserve the --template behaviour and inject the payload as a new thread
    -v, --var-name        <value>    Specify a custom variable name to use for certain output formats
    -t, --timeout         <second>   The number of seconds to wait when reading the payload from STDIN (default 30, 0 to disable)
        --refresh-cache              Rebuild the module metadata cache from disk before listing
    -h, --help                       Show this message
```

### `msfdb` (`.tmp_msf_help/msfdb_help_reconstructed.txt`)

```text
Usage: msfdb [options] <command>
Manage a Metasploit Framework database and web service

General Options:
        --component COMPONENT        Component used with provided command (default: database)
                                       (database, webservice)
    -d, --debug                      Enable debug output
    -h, --help                       Show this help message
        --use-defaults               Accept all defaults and do not prompt for options during an init

Database Options:
        --msf-db-name NAME           Database name (default: msf)
        --msf-db-user-name USER      Database username (default: msf)
        --msf-test-db-name NAME      Test database name (default: msftest)
        --msf-test-db-user-name USER Test database username (default: msftest)
        --db-port PORT               Database port (default: 5432)
        --db-pool MAX                Database connection pool size (default: 200)
        --connection-string URI      Use a pre-existing database cluster for initialization
                                     Example: --connection-string=postgresql://postgres:mysecretpassword@localhost:5432/postgres

Web Service Options:
    -a, --address ADDRESS            Bind to host address (default: 127.0.0.1)
    -p, --port PORT                  Web service port (default: 8080)
        --[no-]daemon                Enable daemon
        --[no-]ssl                   Enable SSL (default: true)
        --ssl-key-file PATH          Path to private key
        --ssl-cert-file PATH         Path to certificate
        --[no-]ssl-disable-verify    Disables (optional) client cert requests
        --environment ENV            Web service framework environment (default: production)
                                       (development, production, test)
        --retry-max MAX              Maximum number of web service connect attempts
        --retry-delay DELAY          Delay in seconds between web service connect attempts
        --user USER                  Initial web service admin username
        --pass PASS                  Initial web service admin password
        --[no-]msf-data-service NAME Local msfconsole data service connection name

Commands:
  init     initialize the component
  reinit   delete and reinitialize the component
  delete   delete and stop the component
  status   check component status
  start    start the component
  stop     stop the component
  restart  restart the component
```

---

## Companion binaries (`bin/*.bat`)

Present in this package under `.tools/metasploit/framework/bin/`:

| Wrapper | Role (package presence) |
|---------|-------------------------|
| `msfconsole.bat` | Primary console — OptionParser reconstructed above |
| `msfvenom.bat` | Payload generator — OptionParser reconstructed above |
| `msfdb.bat` | DB / webservice manager — OptionParser reconstructed above |
| `msfrpcd.bat` / `msfrpc.bat` | RPC daemon / client companions |
| `msfupdate.bat` / `msfupdate.ps1` | Updater (live capture failed with error **1602**) |
| `msfbinscan.bat`, `msfelfscan.bat`, `msfmachscan.bat`, `msfpescan.bat` | Binary format scanners |
| `msfrop.bat` | ROP helper |
| `msfd.bat` | MSF daemon companion |
| `msfremove.bat` / `msfremove.ps1` | Removal helpers |

OptionParser help for companions other than msfconsole / msfvenom / msfdb was **not** reconstructed in this capture pass — do not invent their flags here.

---

## Interactive console command families

Not process argv. Used at the `msf6 >` prompt, inside `-r` resource files, or via `-x`.

| Family | Commands |
|--------|----------|
| Find / load | `search`, `use`, `back` |
| Metadata | `info`, `info -d`, `show options`, `show advanced`, `show evasion`, `show payloads`, `show targets` |
| Datastore | `set`, `setg`, `unset`, `unsetg`, `get`, `getg` |
| Execute | `run`, `check`, `exploit`, `jobs` |
| Sessions | `sessions`, `sessions -l`, `sessions -i`, `sessions -k` |
| Workspace / DB | `workspace`, `db_status`, `db_nmap`, `db_import`, `db_export` |
| Tables | `hosts`, `services`, `vulns`, `creds`, `loot`, `notes` |

### Ranges (shipped `msfconsole.md`)

From package documentation captured as `.tmp_msf_help/msfconsole.md`:

- ID lists: comma-separated; ranges with `-` or `..` (no spaces around commas).
- IP targets: space/comma lists, `BEGIN-END`, full-form CIDR (`127.0.0.0/8`), Nmap-style octet ranges, IPv6; domain/`netmask` forms supported as documented there.

Examples from that file:

```text
sessions -k 1
jobs -k 2-6,7,8,11..15
check 127.168.0.0/16, 127.0.0-2.1-4,15 127.0.0.255
set RHOSTS fe80::3990:0000/110, ::1-::f0f0
set RHOSTS www.example.test/24
```

---

## Re-capture / reconstruct

When a working install is available:

```powershell
$bin = "C:\projects\spiderfeet\.tools\metasploit\framework\bin"
& "$bin\msfconsole.bat" -h 2>&1 | Out-File -Encoding utf8 .tmp_msf_help\msfconsole_h.txt
& "$bin\msfvenom.bat" -h 2>&1 | Out-File -Encoding utf8 .tmp_msf_help\msfvenom_h.txt
& "$bin\msfdb.bat" -h 2>&1 | Out-File -Encoding utf8 .tmp_msf_help\msfdb_h.txt
```

Reconstruct OptionParser help without full Bundler boot (current method):

```powershell
$ruby = "C:\projects\spiderfeet\.tools\metasploit\framework\embedded\bin\ruby.exe"
& $ruby .tmp_msf_help\emit_help.rb .tmp_msf_help
```

Replace the reconstructed sections in this document after any package upgrade — do not merge flags from newer docs without a new capture.
