# Nosey Parker CLI Options

Operator reference for `noseyparker` **v0.24.0**. Prefer structured report export for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
# Scan into an engagement datastore (default path: datastore.np)
noseyparker scan -d ./datastore.np ./target

# Overview (human or structured aggregates)
noseyparker summarize -d ./datastore.np
noseyparker summarize -d ./datastore.np -f json

# Primary structured export for graphs / harvest (not human-only)
noseyparker report -d ./datastore.np -f json -o findings.json
noseyparker report -d ./datastore.np -f jsonl -o findings.jsonl
```

| Field | Value |
|-------|-------|
| Version | **0.24.0** (commit `61fa4ca`, built 2025-05-08) |
| Binary | `/home/brett/.local/spiderfeet-cli/bin/noseyparker` (WSL) |
| Platform | `x86_64-unknown-linux-gnu` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_noseyparker_help/*.txt` |

> Upstream Nosey Parker is retired in favour of [Titus](https://github.com/praetorian-inc/titus). Flags below are from live `--help` on v0.24.0 only — do not invent options.

---

## Captured help

Live help text captured from `/home/brett/.local/spiderfeet-cli/bin/noseyparker` on **2026-08-10**. Each block is the full stdout of the listed command (global options repeated by the CLI are retained).

### Root (`noseyparker --help`)

```text
Nosey Parker is a command-line program that finds secrets and sensitive information in textual data
and Git history.

Usage: noseyparker [OPTIONS] <COMMAND>

Commands:
  scan         Scan content for secrets
  summarize    Summarize scan findings
  report       Report detailed scan findings
  github       Interact with GitHub
  datastore    Manage datastores
  rules        Manage rules and rulesets
  annotations  Manage annotations (experimental)
  generate     Generate Nosey Parker release assets
  help         Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `scan`

```text
Scan content for secrets

This command uses regex-based rules to identify hardcoded secrets and other potentially sensitive
information in textual content (or in inputs that can have textual content extracted from them).

The findings from scanning are recorded into a datastore. The recorded findings can later be
reported in several formats using the `summarize` and `report` commands.

Several types of inputs can be specified:

- Positional input arguments can be either files or directories. Files are scanned directly;
directories are recursively enumerated and scanned. Any directories encountered that are Git
repositories will have their entire history scanned.

- A Git repository URL can be specified with the `--git-repo=URL` argument. This will cause Nosey
Parker to clone that repository to its datastore and scan its history.

- A GitHub user can be specified with the `--github-user=NAME` argument. This will cause Nosey
Parker to enumerate accessible repositories belonging to that user, clone them to its datastore, and
scan their entire history.

- A GitHub organization can be specified with the `--github-org=NAME` argument. This will cause
Nosey Parker to enumerate accessible repositories belonging to that organization, clone them to its
datastore, and scan their entire history.

The `git` binary on the PATH is used to clone any required Git repositories. It is careful invoked
to avoid using any system-wide or user-specific configuration.

By default, when cloning repositories from GitHub or enumerating GitHub users or organizations,
unauthenticated access is used. An optional personal access token can be specified using the
`NP_GITHUB_TOKEN` environment variable. Using a personal access token gives higher rate limits and
may make additional content accessible.

Usage: noseyparker scan [OPTIONS] [INPUT]...

Options:
  -d, --datastore <PATH>
          Use the specified datastore
          
          The datastore will be created if it does not exist.
          
          [env: NP_DATASTORE=]
          [default: datastore.np]

  -j, --jobs <N>
          Use N parallel scanning threads
          
          [default: 3]

  -h, --help
          Print help (see a summary with '-h')

Rule Selection Options:
      --rules-path <PATH>
          Load additional rules and rulesets from the specified file or directory
          
          The paths can be either files or directories. Directories are recursively walked and all
          discovered YAML files of rules and rulesets will be loaded.
          
          This option can be repeated.

      --ruleset <ID>
          Enable the ruleset with the specified ID
          
          The ID must resolve to a built-in ruleset or to an additional ruleset loaded with the
          `--rules=PATH` option.
          
          The special `all` ID causes all loaded rules to be used.
          
          This option can be repeated.
          
          Specifying this option disables the default ruleset. If you want to use a custom ruleset
          in addition to the default ruleset, specify this option twice, e.g., `--ruleset default
          --ruleset CUSTOM_ID`.
          
          [default: default]

      --load-builtins <BOOL>
          Control whether built-in rules and rulesets are loaded
          
          [default: true]
          [possible values: true, false]

Input Specifier Options:
  [INPUT]...
          Scan the specified file, directory, or local Git repository

      --git-url <URL>
          Clone and scan the Git repository at the specified URL
          
          Only https URLs without credentials, query parameters, or fragment identifiers are
          supported.
          
          This option can be repeated.

      --github-repo-type <TYPE>
          Clone and scan GitHub repos only of the given type
          
          [default: source]

          Possible values:
          - all:    Select both source repositories and fork repositories
          - source: Only source repositories, i.e., ones that are not forks
          - fork:   Only fork repositories

      --enumerator <PATH>
          Read inputs from a JSONL enumerator file (experimental)
          
          This can be used to stream inputs from other processes without having to write them to
          disk. Shell process substitution (e.g., `--enumerator=<(my-enumerator-program)`) can make
          this ergonomic.
          
          Each line of the enumerator file should be a JSON object with one of the following forms:
          
          { "content_base64": "base64-encoded bytestring to scan", "provenance": <arbitrary object>
          } { "content": "utf8 string to scan", "provenance": <arbitrary object> }
          
          This option can be repeated.

      --github-organization <NAME>
          Clone and scan accessible repositories belonging to the specified GitHub organization
          
          This option can be repeated.
          
          [aliases: github-org]

      --github-user <NAME>
          Clone and scan accessible repositories belonging to the specified GitHub user
          
          This option can be repeated.

      --all-github-organizations
          Clone and scan accessible repositories from all accessible GitHub organizations
          
          This only works with a GitHub Enterprise Server instance. A non-default option for the
          `--github-api-url` option must be specified.
          
          [aliases: all-github-orgs]

      --github-api-url <URL>
          Use the specified URL for GitHub API access
          
          If accessing a GitHub Enterprise Server instance, this value should be the entire base URL
          include the `api/v3` portion, e.g., `https://github.example.com/api/v3`.
          
          [default: https://api.github.com/]
          [aliases: api-url]

      --git-clone <MODE>
          Use the specified method for cloning Git repositories
          
          [default: bare]

          Possible values:
          - bare:   Match the behavior of `git clone --bare`
          - mirror: Match the behavior of `git clone --mirror`

      --git-history <MODE>
          Use the specified mode for handling Git history
          
          Git history can be completely ignored when scanning by using `--git-history=none`. Note
          that this will interfere with other input specifiers that cause Git repositories to be
          automatically cloned. For example, specifying an input with `--git-url=<URL>` while
          simultaneously using `--git-history=none` will not result in useful scanning.
          
          [default: full]

          Possible values:
          - full: Scan all history
          - none: Scan no history

Content Filtering Options:
      --max-file-size <MEGABYTES>
          Do not scan files larger than the specified size
          
          The value is parsed as a floating point literal, and hence fractional values can be
          supplied. A non-positive value means "no limit". Note that scanning requires reading the
          entire contents of each file into memory, so using an excessively large limit may be
          problematic.
          
          [default: 100]

  -i, --ignore <FILE>
          Use custom path-based ignore rules from the specified file
          
          The ignore file should contain gitignore-style rules.
          
          This option can be repeated.

Metadata Collection Options:
      --blob-metadata <MODE>
          Specify which blobs will have metadata recorded
          
          [default: matching]

          Possible values:
          - all:      Record metadata for all encountered blobs
          - matching: Record metadata only for blobs with matches
          - none:     Record metadata for no blobs

      --git-blob-provenance <MODE>
          Specify which Git commit provenance metadata will be collected
          
          This should not need to be changed unless you are running into performance problems on a
          problematic Git repository input.
          
          [default: first-seen]

          Possible values:
          - first-seen: The Git repository and set of commits and accompanying pathnames in which a
            blob is first seen
          - minimal:    Only the Git repository in which a blob is seen

      --copy-blobs-format <FORMAT>
          Specify the format for blobs copied by the `--copy-blobs` option
          
          [default: parquet]

          Possible values:
          - parquet: Parquet format
          - files:   Plain files, similar to Git's loose object format

Data Collection Options:
      --snippet-length <BYTES>
          Include up to the specified number of bytes before and after each match
          
          The default value typically gives between 4 and 7 lines of context before and after each
          match.
          
          [default: 256]

      --copy-blobs <MODE>
          Specify which blobs will be copied in entirety to the datastore
          
          If this option is enabled, corresponding blobs will be written to the `blobs` directory
          within the datastore. The format of that directory is similar to Git's "loose" object
          format: the first 2 characters of the hex-encoded blob ID name a subdirectory, and the
          remaining characters are used as the filename.
          
          This mechanism exists to aid in ad-hoc downstream investigation. Copied blobs are not used
          elsewhere in Nosey Parker at this point.
          
          [default: none]

          Possible values:
          - all:      Copy all encountered blobs
          - matching: Copy only blobs with matches
          - none:     Copy no blobs

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `summarize`

```text
Summarize scan findings

Findings are summarized in tabular form. The default `human` format prints a table of findings with
one row for each rule that produced findings. The table has several columns:

- Rule: the name of the rule

- Findings: the number of findings, i.e., the number of distinct match group values produced by the
rule

- Matches: the number of individual matches

- Accepted: the number of findings whose matches have `accept` status

- Rejected: the number of findings whose matches have `reject` status

- Mixed: the number of findings whose matches have a mix of `accept` and `reject` status

- Unlabeled: the number of findings whose matches have no status at all

Usage: noseyparker summarize [OPTIONS]

Options:
  -d, --datastore <PATH>
          Use the specified datastore
          
          [env: NP_DATASTORE=]
          [default: datastore.np]

  -h, --help
          Print help (see a summary with '-h')

Output Options:
  -o, --output <PATH>
          Write output to the specified path
          
          If this argument is not provided, stdout will be used.

  -f, --format <FORMAT>
          Write output in the specified format
          
          [default: human]

          Possible values:
          - human: A text-based format designed for humans
          - json:  Pretty-printed JSON format
          - jsonl: JSON Lines format

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `report`

```text
Report detailed scan findings

Usage: noseyparker report [OPTIONS]

Options:
  -d, --datastore <PATH>
          Use the specified datastore
          
          [env: NP_DATASTORE=]
          [default: datastore.np]

  -h, --help
          Print help (see a summary with '-h')

Filtering Options:
      --max-matches <N>
          Limit the number of matches per finding to at most N
          
          A non-positive value means "no limit".
          
          [default: 3]

      --max-provenance <N>
          Limit the number of provenance entries per match to at most N
          
          A non-positive value means "no limit".
          
          [default: 3]

      --min-score <SCORE>
          Only report findings that have a mean score of at least N
          
          Scores are floating point numbers in the range [0, 1]. Use the value `0` to disable this
          filtering.
          
          Findings that do not have a score computed will be included regardless of this setting.
          
          [default: 0.05]

      --finding-status <STATUS>
          Include only findings with the assigned status

          Possible values:
          - accept: Findings with `accept` matches
          - reject: Findings with `reject` matches
          - mixed:  Findings with both `accept` and `reject` matches
          - null:   Findings without any `accept` or `reject` matches

      --suppress-redundant <BOOL>
          Suppress redundant matches and findings
          
          A match is considered redundant to another if they overlap significantly within the same
          blob and satisfy a handful of heuristics.
          
          [default: true]
          [possible values: true, false]

Output Options:
  -o, --output <PATH>
          Write output to the specified path
          
          If this argument is not provided, stdout will be used.

  -f, --format <FORMAT>
          Write output in the specified format
          
          [default: human]

          Possible values:
          - human: A text-based format designed for humans
          - json:  Pretty-printed JSON format
          - jsonl: JSON Lines format
          - sarif: SARIF format (experimental)

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `github`

```text
Interact with GitHub

By default, unauthenticated access is used. An optional personal access token can be specified using
the `NP_GITHUB_TOKEN` environment variable. Using a personal access token gives higher rate limits
and may make additional content accessible.

Usage: noseyparker github [OPTIONS] <COMMAND>

Commands:
  repos  Interact with GitHub repositories
  help   Print this message or the help of the given subcommand(s)

Options:
      --github-api-url <URL>
          Use the specified URL for GitHub API access
          
          If accessing a GitHub Enterprise Server instance, this value should be the entire base URL
          include the `api/v3` portion, e.g., `https://github.example.com/api/v3`.
          
          [default: https://api.github.com/]
          [aliases: api-url]

  -h, --help
          Print help (see a summary with '-h')

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `datastore`

```text
Manage datastores

Usage: noseyparker datastore [OPTIONS] <COMMAND>

Commands:
  init    Initialize a new datastore
  export  Export a datastore
  help    Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `rules`

```text
Manage rules and rulesets

Usage: noseyparker rules [OPTIONS] <COMMAND>

Commands:
  check  Check rules for problems
  list   List available rules
  help   Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `annotations`

```text
Manage annotations (experimental)

Annotations include assigned status (`accept` or `reject`) and freeform comments.

Usage: noseyparker annotations [OPTIONS] <COMMAND>

Commands:
  export  Export annotations from a datastore (experimental)
  import  Import annotations into a datastore (experimental)
  help    Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

### `generate`

```text
Generate Nosey Parker release assets

This command is used primarily for generation of artifacts to be included in releases.

Usage: noseyparker generate [OPTIONS] <COMMAND>

Commands:
  manpages           Generate man pages
  json-schema        Generate the JSON schema for the output of the `report` command
  shell-completions  Generate shell completions
  help               Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

Global Options:
  -v, --verbose...
          Enable verbose output
          
          This can be repeated up to 3 times to enable successively more output.

  -q, --quiet
          Suppress non-error feedback messages
          
          This silences WARNING, INFO, DEBUG, and TRACE messages and disables progress bars. This
          overrides any provided verbosity and progress reporting options.

      --color <MODE>
          Enable or disable colored output
          
          When this is "auto", colors are enabled for stdout and stderr when they are terminals.
          
          If the `NO_COLOR` environment variable is set, it takes precedence and is equivalent to
          `--color=never`.
          
          [default: auto]
          [possible values: auto, never, always]

      --progress <MODE>
          Enable or disable progress bars
          
          When this is "auto", progress bars are enabled when stderr is a terminal.
          
          [default: auto]
          [possible values: auto, never, always]

      --ignore-certs
          Ignore validation of TLS certificates

Advanced Global Options:
      --rlimit-nofile <LIMIT>
          Set the rlimit for number of open files to LIMIT
          
          This should not need to be changed from the default unless you run into crashes from
          running out of file descriptors.
          
          [default: 16384]

      --sqlite-cache-size <SIZE>
          Set the cache size for SQLite connections to SIZE
          
          This has the effect of setting SQLite's `pragma cache_size=SIZE`. The default value is set
          to use a maximum of 1GiB for database cache. See
          <https://sqlite.org/pragma.html#pragma_cache_size> for more details.
          
          [default: -1048576]

      --enable-backtraces <BOOL>
          Enable or disable backtraces on panic
          
          This has the effect of setting the `RUST_BACKTRACE` environment variable to 1.
          
          [default: true]
          [possible values: true, false]
```

---

## Re-capture commands

```bash
NP=/home/brett/.local/spiderfeet-cli/bin/noseyparker
OUT=/mnt/c/projects/spiderfeet/.tmp_noseyparker_help
mkdir -p "$OUT"
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

# Optional single-file dump used by the repo capture script
bash /mnt/c/projects/spiderfeet/.seed/scripts/capture_noseyparker_help.sh /tmp/noseyparker_help_capture.txt
```

From PowerShell (WSL wrapper):

```powershell
wsl bash -lc '~/.local/spiderfeet-cli/bin/noseyparker --help'
wsl bash -lc '~/.local/spiderfeet-cli/bin/noseyparker scan --help'
wsl bash -lc '~/.local/spiderfeet-cli/bin/noseyparker report --help'
```

---

## Curated option tables

Summaries of the most-used flags from the captured help above. Prefer the Captured help blocks when wording must match the binary exactly.

### Command tree

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

### Environment

| Variable | Purpose |
|----------|---------|
| `NP_DATASTORE` | Default `-d` / `--datastore` path (`datastore.np`) |
| `NP_GITHUB_TOKEN` | GitHub PAT for clone/enumerate rate limits and private access |
| `NO_COLOR` | Equivalent to `--color=never` |

### Global options (all subcommands)

| Option | Description |
|--------|-------------|
| `-v`, `--verbose` | Repeat up to 3× for more detail |
| `-q`, `--quiet` | Suppress non-error feedback; disables progress bars |
| `--color auto|never|always` | Coloured output (default `auto`) |
| `--progress auto|never|always` | Progress bars when stderr is a TTY |
| `--ignore-certs` | Skip TLS certificate validation |
| `--rlimit-nofile <LIMIT>` | Open-file rlimit (default `16384`) |
| `--sqlite-cache-size <SIZE>` | SQLite `pragma cache_size` (default `-1048576`) |
| `--enable-backtraces true|false` | Panic backtraces (default `true`) |

### `scan` — inputs

| Option | Description |
|--------|-------------|
| `[INPUT]...` | Local file, directory, or Git repository |
| `--git-url <URL>` | Clone and scan HTTPS Git URL (repeatable; no credentials/query/fragment) |
| `--github-user <NAME>` | Clone/scan accessible user repositories (repeatable) |
| `--github-organization <NAME>` | Clone/scan org repositories (`--github-org`; repeatable) |
| `--all-github-organizations` | All accessible orgs (GHES + non-default `--github-api-url`) |
| `--github-api-url <URL>` | API base (default `https://api.github.com/`; GHES needs `/api/v3`) |
| `--github-repo-type all|source|fork` | Repo filter (default `source`) |
| `--enumerator <PATH>` | Experimental JSONL enumerator (`content` / `content_base64` + `provenance`) |
| `--git-clone bare|mirror` | Clone method (default `bare`) |
| `--git-history full|none` | History mode (default `full`; `none` breaks useful `--git-url` scans) |

### `scan` — rules, filters, collection

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--datastore` | `datastore.np` | Datastore path (created if missing) |
| `-j`, `--jobs` | `3` | Parallel scanning threads |
| `--rules-path <PATH>` | — | Load extra YAML rules/rulesets (repeatable) |
| `--ruleset <ID>` | `default` | Enable ruleset; `all` = every loaded rule |
| `--load-builtins` | `true` | Load built-in rules/rulesets |
| `--max-file-size` | `100` | Skip larger files (MiB); ≤0 = no limit |
| `-i`, `--ignore` | — | Gitignore-style ignore file (repeatable) |
| `--snippet-length` | `256` | Context bytes around each match |
| `--blob-metadata` | `matching` | `all` / `matching` / `none` |
| `--git-blob-provenance` | `first-seen` | `first-seen` / `minimal` |
| `--copy-blobs` | `none` | `all` / `matching` / `none` |
| `--copy-blobs-format` | `parquet` | `parquet` / `files` |

### `summarize` / `report` — output

| Option | Commands | Notes |
|--------|----------|-------|
| `-d`, `--datastore` | both | Same env default as scan |
| `-o`, `--output` | both | File path; stdout if omitted |
| `-f human` | both | Default human tables / detail |
| `-f json` | both | Pretty-printed JSON |
| `-f jsonl` | both | JSON Lines — preferred for pipelines |
| `-f sarif` | report only | Experimental SARIF |

### `report` — filtering

| Option | Default | Description |
|--------|---------|-------------|
| `--max-matches` | `3` | Cap matches per finding (≤0 = unlimited) |
| `--max-provenance` | `3` | Cap provenance entries per match |
| `--min-score` | `0.05` | Mean score threshold `[0,1]`; `0` disables |
| `--finding-status` | — | `accept` / `reject` / `mixed` / `null` |
| `--suppress-redundant` | `true` | Collapse overlapping matches in a blob |

### Nested commands (see live `--help` for full flags)

| Command | Role |
|---------|------|
| `github repos` | Interact with GitHub repositories (list before full org scan) |
| `datastore init` | Initialize a new datastore |
| `datastore export` | Export a datastore archive |
| `rules check` | Validate custom rules |
| `rules list` | List available rules |
| `annotations export` / `import` | Experimental accept/reject + comments |
| `generate json-schema` | JSON schema for `report` output |
| `generate manpages` / `shell-completions` | Release assets |

---

## Examples

```bash
# Local repo (Git history scanned automatically when .git present)
noseyparker scan -d ./np.np ./myapp
noseyparker summarize -d ./np.np
noseyparker report -d ./np.np -f jsonl -o findings.jsonl

# Remote HTTPS clone
noseyparker scan -d ./np.np --git-url https://github.com/org/service

# Authorized GitHub org
export NP_GITHUB_TOKEN=ghp_...
noseyparker scan -d ./np.np --github-organization acme --github-repo-type source

# High-signal JSONL
noseyparker report -d ./np.np -f jsonl --min-score 0.2 --finding-status null -o high.jsonl

# Custom rules alongside default
noseyparker scan -d ./np.np --rules-path ./rules/ --ruleset default --ruleset internal ./target/

# Filesystem only
noseyparker scan -d ./np.np --git-history=none ./checkout

# Docker
docker run -v "$PWD":/scan -w /scan ghcr.io/praetorian-inc/noseyparker:v0.24.0 \
  scan -d /scan/np.np /scan/repo
```

---

## See also

- `.docs/docs-for-cli-tools/Nosey-Parker-Zero-to-Hero.md`
- `.cursor/skills/nosey_parker/SKILL.md`
- `.cursor/skills/nosey_parker/references/`
- `.cursor/skills/Titus/SKILL.md` (successor tool)
