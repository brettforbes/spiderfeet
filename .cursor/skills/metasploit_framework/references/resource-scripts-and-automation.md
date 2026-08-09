# Resource Scripts and Automation

## Entrypoints (msfconsole argv)

From reconstructed OptionParser (**2026-08-10**):

| Flag | Behaviour |
|------|-----------|
| `-r`, `--resource FILE` | Execute resource file; `-` means stdin |
| `-x`, `--execute-command COMMAND` | Run console commands; use `;` for multiples |
| `-q`, `--quiet` | Suppress banner (preferred in automation) |
| `-o`, `--output FILE` | Tee console output to file |
| `-n`, `--no-database` | Disable DB (only when intentional) |

Examples:

```bash
msfconsole -q -r discover.rc
msfconsole -q -x "workspace lab1; db_status; hosts"
cat discover.rc | msfconsole -q -r -
```

## Resource script shape

```text
# discover.rc — always pin workspace first
workspace lab1
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.56.0/24
set THREADS 8
run
hosts
services
```

Best practices:

- Deterministic steps: `workspace` → `use` → `set` → `run` → report commands.
- Avoid interactive prompts; use `--use-defaults` for `msfdb init` outside the script.
- Prefer DB tables + `db_export` over scraping banners.
- Keep one scenario per script for corpus clarity.

## When automation fails on Windows extract

If Bundler raises `GemNotFound`, the resource script never runs — capture the failure as an error scenario; do not treat empty output as a clean miss.
