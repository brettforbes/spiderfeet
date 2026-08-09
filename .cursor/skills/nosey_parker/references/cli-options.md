# nosey_parker CLI Options (summary)

Full live Captured help (exact `--help` text): `.docs/docs-for-cli-tools/Nosey-Parker-CLI-Options.md`

**Binary:** `/home/brett/.local/spiderfeet-cli/bin/noseyparker` (WSL) · **v0.24.0** · captured **2026-08-10**. **Windows:** WSL or Docker only.

## Command tree

```
noseyparker
├── scan
├── summarize
├── report
├── github
│   └── repos
├── datastore
│   ├── init
│   └── export
├── rules
│   ├── check
│   └── list
├── annotations (experimental)
│   ├── export
│   └── import
└── generate
    ├── manpages
    ├── json-schema
    └── shell-completions
```

## Global options (all subcommands)

| Option | Description |
|--------|-------------|
| `-v`, `--verbose` | Repeat up to 3× for more detail |
| `-q`, `--quiet` | Suppress non-error output; disables progress bars |
| `--color auto\|never\|always` | Terminal colour (default `auto`; `NO_COLOR` wins) |
| `--progress auto\|never\|always` | Progress bars on stderr |
| `--ignore-certs` | Skip TLS certificate validation |
| `--rlimit-nofile` | Open-file rlimit (default 16384) |
| `--sqlite-cache-size` | SQLite cache pragma (default ~1 GiB) |
| `--enable-backtraces` | Set `RUST_BACKTRACE` on panic (default true) |

## Environment

| Variable | Used by |
|----------|---------|
| `NP_DATASTORE` | Default `-d` path (`datastore.np`) |
| `NP_GITHUB_TOKEN` | GitHub clone/enumerate |
| `NO_COLOR` | Colour disable |

## SpiderFeet defaults

```bash
noseyparker scan -d ./datastore.np ./target
noseyparker report -d ./datastore.np -f jsonl -o findings.jsonl
# also acceptable: -f json
```

## Scan inputs (exact flag names)

| Specifier | Flag |
|-----------|------|
| Local path / Git repo | positional `[INPUT]...` |
| Remote Git HTTPS | `--git-url` |
| GitHub user | `--github-user` |
| GitHub organization | `--github-organization` (`--github-org`) |
| Enumerator JSONL | `--enumerator` |

## Re-capture help

```bash
NP=/home/brett/.local/spiderfeet-cli/bin/noseyparker
OUT=/mnt/c/projects/spiderfeet/.tmp_noseyparker_help
"$NP" --version | tee "$OUT/version.txt"
"$NP" --help > "$OUT/root_help.txt"
"$NP" scan --help > "$OUT/scan_help.txt"
"$NP" summarize --help > "$OUT/summarize_help.txt"
"$NP" report --help > "$OUT/report_help.txt"
"$NP" github --help > "$OUT/github_help.txt"
"$NP" datastore --help > "$OUT/datastore_help.txt"
"$NP" rules --help > "$OUT/rules_help.txt"
"$NP" annotations --help > "$OUT/annotations_help.txt"
"$NP" generate --help > "$OUT/generate_help.txt"
```
