# Automation and Scripting

## SpiderFeet preference: `recon-cli`

For corpus harvest, CI, and non-interactive pipelines, prefer **`recon-cli`** with explicit `-w`, `-m`, `-o` / `-g`, and `-x`.

Captured flags (do not invent others): `-C`, `-c`, `-G`, `-g`, `-M`, `-m`, `-O`, `-o`, `-x`, plus workspace and `--no-*` / `--stealth` / `--version`.

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
$cli = "C:\projects\spiderfeet\.tools\recon-ng\recon-cli"

& $py $cli -w acme-ext -G
& $py $cli -w acme-ext -M
& $py $cli -w acme-ext -m recon/domains-hosts/<module> -O
& $py $cli -w acme-ext -m recon/domains-hosts/<module> -o SOURCE=example.com -x
& $py $cli -w acme-ext -C "db query SELECT COUNT(*) FROM hosts"
```

`-C` runs a command in global context; `-c` runs in module context (pre-run).

## Resource files

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng -w acme-ext -r .\pipelines\acme.rc
```

Use when the command sequence is stable and versioned with the engagement.

## Script record / execute

Interactive console:

- `script record` — capture a validated manual session
- `script execute` — replay

Promote recorded flows to `.rc` or `recon-cli` once stable.

## Spool

`spool` captures console output for audit, troubleshooting, and text-tab evidence. Name files with workspace + timestamp.

## Adaptive gates (required for good automation)

Do not run purely linear chains:

- Empty prerequisite table → skip dependent module
- Zero row delta → pivot module family
- Quota / auth errors → pause paid modules; continue passive where possible

## Diagnostics

- Raise `VERBOSITY` (`-g VERBOSITY=2`) when debugging
- Route framework bugs → recon-ng issues; module bugs → marketplace issues
- Keep logs with workspace IDs for reproducibility

## Empty modules under stealth

If automation uses `--stealth` before marketplace install, `-M` shows no modules. Install modules with marketplace enabled first (see `cli-options.md`).
